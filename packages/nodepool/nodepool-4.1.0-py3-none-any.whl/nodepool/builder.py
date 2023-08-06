# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import fcntl
import logging
import os
import select
import shutil
import socket
import subprocess
import threading
import time
import shlex
import uuid

from pathlib import Path

from nodepool import config as nodepool_config
from nodepool import exceptions
from nodepool import provider_manager
from nodepool import stats
from nodepool import zk


MINS = 60
HOURS = 60 * MINS
# How long to wait for an image save
IMAGE_TIMEOUT = 6 * HOURS

# How long to wait between checks for ZooKeeper connectivity if it disappears.
SUSPEND_WAIT_TIME = 30

# HP Cloud requires qemu compat with 0.10. That version works elsewhere,
# so just hardcode it for all qcow2 building
DEFAULT_QEMU_IMAGE_COMPAT_OPTIONS = "--qemu-img-options 'compat=0.10'"

# DIB process polling timeout, in milliseconds
BUILD_PROCESS_POLL_TIMEOUT = 30 * 1000


class DibImageFile(object):
    '''
    Class used as an API to finding locally built DIB image files, and
    also used to represent the found files. Image files are named using
    a unique ID, but can be available in multiple formats (with different
    extensions).
    '''
    def __init__(self, image_id, extension=None):
        self.image_id = image_id
        self.extension = extension
        self.md5 = None
        self.md5_file = None
        self.sha256 = None
        self.sha256_file = None

        # File extension is compared to image type (sans '.') so we
        # store it the same way.
        if self.extension:
            self.extension = self.extension.lstrip('.')

    @staticmethod
    def from_path(path):
        if isinstance(path, str):
            path = Path(path)
        return DibImageFile(path.stem, path.suffix)

    @staticmethod
    def from_image_id(images_dir, image_id):
        images = []
        for image_file in Path(images_dir).iterdir():
            if image_file.is_file():
                image = DibImageFile.from_path(image_file)
                if image.image_id == image_id:
                    images.append(image)
        return images

    @staticmethod
    def from_images_dir(images_dir):
        return [DibImageFile.from_path(x) for x in Path(images_dir).iterdir()]

    def to_path(self, images_dir, with_extension=True):
        my_path = Path(images_dir) / self.image_id
        if with_extension:
            if self.extension is None:
                raise exceptions.BuilderError(
                    'Cannot specify image extension of None'
                )
            my_path = my_path.with_suffix('.' + self.extension)

        # Path.with_suffix() will replace an existing suffix, so we create
        # new Path objects from strings for the checksum files.
        md5_path = Path(str(my_path) + '.md5')
        md5 = self._checksum(md5_path)
        if md5:
            self.md5_file = str(md5_path)
            self.md5 = md5[0:32]

        sha256_path = Path(str(my_path) + '.sha256')
        sha256 = self._checksum(sha256_path)
        if sha256:
            self.sha256_file = str(sha256_path)
            self.sha256 = sha256[0:64]

        return str(my_path)

    def _checksum(self, filename):
        if filename.is_file():
            return filename.read_text()
        return None


class BaseWorker(threading.Thread):
    def __init__(self, builder_id, config_path, secure_path, interval, zk):
        super(BaseWorker, self).__init__()
        self.log = logging.getLogger("nodepool.builder.BaseWorker")
        self.daemon = True
        self._running = False
        self._stop_event = threading.Event()
        self._config = None
        self._config_path = config_path
        self._secure_path = secure_path
        self._zk = zk
        self._hostname = socket.getfqdn()
        self._statsd = stats.get_client()
        self._interval = interval
        self._builder_id = builder_id

    def _checkForZooKeeperChanges(self, new_config):
        '''
        Check config for ZooKeeper cluster changes.

        If the defined set of ZooKeeper servers changes, the connection
        will use the new server set.
        '''
        if self._config.zookeeper_servers != new_config.zookeeper_servers:
            self.log.debug("Detected ZooKeeper server changes")
            self._zk.resetHosts(list(new_config.zookeeper_servers.values()))

    def _readConfig(self):
        new_config = nodepool_config.loadConfig(self._config_path)
        if self._secure_path:
            nodepool_config.loadSecureConfig(new_config, self._secure_path)
        return new_config

    @property
    def running(self):
        return self._running

    def shutdown(self):
        self._running = False
        self._stop_event.set()


class CleanupWorker(BaseWorker):
    '''
    The janitor of nodepool-builder that will remove images from providers
    and any local DIB builds.
    '''

    def __init__(self, name, builder_id, config_path, secure_path,
                 interval, zk):
        super(CleanupWorker, self).__init__(builder_id, config_path,
                                            secure_path, interval, zk)
        self.log = logging.getLogger(
            "nodepool.builder.CleanupWorker.%s" % name)
        self.name = 'CleanupWorker.%s' % name

    def _buildUploadRecencyTable(self):
        '''
        Builds a table for each image of the most recent uploads to each
        provider.

        Example)

            image1:
                providerA: [ (build_id, upload_id, upload_time), ...  ]
                providerB: [ (build_id, upload_id, upload_time), ...  ]
            image2:
                providerC: [ (build_id, upload_id, upload_time), ...  ]
        '''
        self._rtable = {}
        for image in self._zk.getImageNames():
            self._rtable[image] = {}
            for build in self._zk.getBuilds(image, zk.READY):
                for provider in self._zk.getBuildProviders(image, build.id):
                    if provider not in self._rtable[image]:
                        self._rtable[image][provider] = []
                    uploads = self._zk.getMostRecentBuildImageUploads(
                        2, image, build.id, provider, zk.READY)
                    for upload in uploads:
                        self._rtable[image][provider].append(
                            (build.id, upload.id, upload.state_time)
                        )

        # Sort uploads by state_time (upload time) and keep the 2 most recent
        for i in list(self._rtable.keys()):
            for p in self._rtable[i].keys():
                self._rtable[i][p].sort(key=lambda x: x[2], reverse=True)
                self._rtable[i][p] = self._rtable[i][p][:2]

    def _isRecentUpload(self, image, provider, build_id, upload_id):
        '''
        Search for an upload for a build within the recency table.
        '''
        provider = self._rtable[image].get(provider)
        if not provider:
            return False

        for b_id, u_id, u_time in provider:
            if build_id == b_id and upload_id == u_id:
                return True
        return False

    def _inProgressUpload(self, upload):
        '''
        Determine if an upload is in progress.
        '''
        if upload.state != zk.UPLOADING:
            return False

        try:
            with self._zk.imageUploadLock(upload.image_name, upload.build_id,
                                          upload.provider_name,
                                          blocking=False):
                pass
        except exceptions.ZKLockException:
            return True
        return False

    @staticmethod
    def deleteLocalBuild(images_dir, image, build, log):
        '''
        Remove expired image build from local disk.

        It is safe to call this multiple times, or if no local files exist.

        :param str images_dir: Path to the DIB images directory.
        :param str image: Name of the image whose build we are deleting.
        :param ImageBuild build: The build we want to delete.
        :param Logger log: A logging object for log output.
        '''
        def removeDibItem(filename):
            if filename is None:
                return
            try:
                os.remove(filename)
                log.info("Removed DIB file %s" % filename)
            except OSError as e:
                if e.errno != 2:    # No such file or directory
                    raise e

        base = "-".join([image, build.id])
        files = DibImageFile.from_image_id(images_dir, base)
        if not files:
            return

        log.info("Doing cleanup for %s:%s" % (image, build.id))

        manifest_dir = None

        for f in files:
            filename = f.to_path(images_dir, True)
            if not manifest_dir:
                path, ext = filename.rsplit('.', 1)
                manifest_dir = path + ".d"
            items = [filename, f.md5_file, f.sha256_file]
            list(map(removeDibItem, items))

        try:
            shutil.rmtree(manifest_dir)
            log.info("Removed DIB manifest %s" % manifest_dir)
        except OSError as e:
            if e.errno != 2:    # No such file or directory
                raise e

    def _deleteLocalBuild(self, image, build):
        CleanupWorker.deleteLocalBuild(
            self._config.images_dir, image, build, self.log)

    def _cleanupProvider(self, provider, image, build_id):
        all_uploads = self._zk.getUploads(image, build_id, provider.name)

        for upload in all_uploads:
            if self._isRecentUpload(image, provider.name, build_id, upload.id):
                continue
            self.log.debug("Deleting non-recent image upload: %s", upload)
            self._deleteUpload(upload)

    def _cleanupObsoleteProviderUploads(self, provider, image, build_id):
        if image in provider.diskimages:
            # This image is in use for this provider
            return

        all_uploads = self._zk.getUploads(image, build_id, provider.name)
        for upload in all_uploads:
            self.log.debug("Deleting obsolete image upload: %s", upload)
            self._deleteUpload(upload)

    def _deleteUpload(self, upload):
        if upload.state != zk.DELETING:
            if not self._inProgressUpload(upload):
                try:
                    with self._zk.imageUploadNumberLock(upload,
                                                        blocking=False):
                        upload.state = zk.DELETING
                        self._zk.storeImageUpload(upload.image_name,
                                                  upload.build_id,
                                                  upload.provider_name,
                                                  upload,
                                                  upload.id)
                except exceptions.ZKLockException:
                    # If we can't get a lock, we'll try again later.
                    self.log.debug("Unable to get lock on image upload: %s",
                                   upload)
                    return

        if upload.state == zk.DELETING:
            manager = self._config.provider_managers[upload.provider_name]
            try:
                # It is possible we got this far, but don't actually have an
                # external_id. This could mean that zookeeper and cloud
                # provider are some how out of sync.
                if upload.external_id:
                    base = "-".join([upload.image_name, upload.build_id])
                    self.log.info("Deleting image build %s from %s" %
                                  (base, upload.provider_name))
                    manager.deleteImage(upload.external_name,
                                        upload.external_id)
            except Exception:
                self.log.exception(
                    "Unable to delete image %s from %s:",
                    upload.external_name, upload.provider_name)
            else:
                self.log.debug("Deleting image upload: %s", upload)
                try:
                    with self._zk.imageUploadNumberLock(upload,
                                                        blocking=False):
                        self._zk.deleteUpload(upload.image_name,
                                              upload.build_id,
                                              upload.provider_name, upload.id)
                except exceptions.ZKLockException:
                    # If we can't get a lock, we'll try again later.
                    self.log.debug("Unable to get lock on image upload: %s",
                                   upload)

    def _inProgressBuild(self, build, image):
        '''
        Determine if a DIB build is in progress.
        '''
        if build.state != zk.BUILDING:
            return False

        try:
            with self._zk.imageBuildLock(image, blocking=False):
                # An additional state check is needed to make sure it hasn't
                # changed on us. If it has, then let's pretend a build is
                # still in progress so that it is checked again later with
                # its new build state.
                b = self._zk.getBuild(image, build.id)
                if b and b.state != zk.BUILDING:
                    return True
                pass
        except exceptions.ZKLockException:
            return True
        return False

    def _cleanup(self):
        '''
        Clean up builds on disk and in providers.
        '''
        known_providers = self._config.providers.values()
        image_names = self._zk.getImageNames()

        self._buildUploadRecencyTable()

        for image in image_names:
            try:
                self._cleanupImage(known_providers, image)
            except Exception:
                self.log.exception("Exception cleaning up image %s:", image)

    def _filterLocalBuilds(self, image, builds):
        '''Return the subset of builds that are local'''
        ret = []
        for build in builds:
            is_local = build.builder_id == self._builder_id
            if is_local:
                ret.append(build)
        return ret

    def _cleanupCurrentProviderUploads(self, provider, image, build_id):
        '''
        Remove cruft from a current build.

        Current builds (the ones we want to keep) are treated special since
        we want to remove any ZK nodes for uploads that failed exceptionally
        hard (i.e., we could not set the state to FAILED and they remain as
        UPLOADING), and we also want to remove any uploads that have been
        marked for deleting.
        '''
        cruft = self._zk.getUploads(image, build_id, provider,
                                    states=[zk.UPLOADING,
                                            zk.DELETING,
                                            zk.FAILED])
        for upload in cruft:
            if (upload.state == zk.UPLOADING and
                not self._inProgressUpload(upload)
            ):
                # Since we cache the uploads above, we need to verify the
                # state hasn't changed on us (e.g., it could have gone from
                # an in progress upload to a successfully completed upload
                # between the getUploads() and the _inProgressUpload() check.
                u = self._zk.getImageUpload(image, build_id, provider,
                                            upload.id)
                if not u:
                    self.log.warning(
                        "Ignoring invalid or empty image upload: %s", upload
                    )
                    continue
                if upload.state != u.state:
                    continue
                self.log.debug("Removing failed upload record: %s" % upload)
                self._zk.deleteUpload(image, build_id, provider, upload.id)
            elif upload.state == zk.DELETING:
                self.log.debug(
                    "Removing deleted upload and record: %s" % upload)
                self._deleteUpload(upload)
            elif upload.state == zk.FAILED:
                self.log.debug(
                    "Removing failed upload and record: %s" % upload)
                self._deleteUpload(upload)

    def _cleanupImage(self, known_providers, image):
        '''
        Clean up one image.
        '''
        # Get the list of all builds, then work from that so that we
        # have a consistent view of the data.
        all_builds = self._zk.getBuilds(image)
        builds_to_keep = set([b for b in sorted(all_builds, reverse=True,
                                                key=lambda y: y.state_time)
                              if b.state == zk.READY][:2])
        local_builds = set(self._filterLocalBuilds(image, all_builds))
        diskimage = self._config.diskimages.get(image)
        if not diskimage and not local_builds:
            # This builder is not configured to build this image and was not
            # responsible for this image build so ignore it.
            return
        # Remove any local builds that are not in use.
        if not diskimage or (diskimage and not diskimage.image_types):
            builds_to_keep -= local_builds
            # TODO(jeblair): When all builds for an image which is not
            # in use are deleted, the image znode should be deleted as
            # well.

        for build in all_builds:
            # Start by deleting any uploads that are no longer needed
            # because this image has been removed from a provider
            # (since this should be done regardless of the build
            # state).
            for provider in known_providers:
                if not provider.manage_images:
                    # This provider doesn't manage images
                    continue
                try:
                    self._cleanupObsoleteProviderUploads(provider, image,
                                                         build.id)
                    if build in builds_to_keep:
                        self._cleanupCurrentProviderUploads(provider.name,
                                                            image,
                                                            build.id)
                except Exception:
                    self.log.exception("Exception cleaning up uploads "
                                       "of build %s of image %s in "
                                       "provider %s:",
                                       build, image, provider)

            # If the build is in the delete state, we will try to
            # delete the entire thing regardless.
            if build.state != zk.DELETING:
                # If it is in any other state, we will only delete it
                # if it is older than the most recent two ready
                # builds, or is in the building state but not actually
                # building.
                if build in builds_to_keep:
                    continue
                elif self._inProgressBuild(build, image):
                    continue

            for provider in known_providers:
                if not provider.manage_images:
                    # This provider doesn't manage images
                    continue
                try:
                    self._cleanupProvider(provider, image, build.id)
                except Exception:
                    self.log.exception("Exception cleaning up build %s "
                                       "of image %s in provider %s:",
                                       build, image, provider)

            uploads = []
            for p in self._zk.getBuildProviders(image, build.id):
                uploads += self._zk.getUploads(image, build.id, p)

            # If we own this build, delete the local DIB files as soon as all
            # provider uploads are in a deleting state. This prevents us from
            # keeping local files around while we wait on clouds to remove
            # the image on their side (which can be very slow).
            all_deleting = all(map(lambda x: x.state == zk.DELETING, uploads))
            is_local = build.builder_id == self._builder_id
            if (not uploads or all_deleting) and is_local:
                # If we got here, it's either an explicit delete (user
                # activated), or we're deleting because we have newer
                # images.  We're about to start deleting files, so
                # make sure that the dib image state reflects that.
                if build.state != zk.DELETING:
                    with self._zk.imageBuildNumberLock(
                        image, build.id, blocking=False
                    ):
                        build.state = zk.DELETING
                        self._zk.storeBuild(image, build, build.id)

                self._deleteLocalBuild(image, build)

            if not uploads:
                if is_local:
                    # Only remove the db build record from the builder that
                    # built this image. This prevents us from removing the db
                    # record without first removing the local image files.
                    if not self._zk.deleteBuild(image, build.id):
                        self.log.error("Unable to delete build %s because"
                                       " uploads still remain.", build)

    def run(self):
        '''
        Start point for the CleanupWorker thread.
        '''
        self._running = True
        while self._running:
            # Don't do work if we've lost communication with the ZK cluster
            did_suspend = False
            while self._zk and (self._zk.suspended or self._zk.lost):
                did_suspend = True
                self.log.info("ZooKeeper suspended. Waiting")
                time.sleep(SUSPEND_WAIT_TIME)
            if did_suspend:
                self.log.info("ZooKeeper available. Resuming")

            try:
                self._run()
            except Exception:
                self.log.exception("Exception in CleanupWorker:")
                time.sleep(10)

            self._stop_event.wait(self._interval)

        provider_manager.ProviderManager.stopProviders(self._config)

    def _run(self):
        '''
        Body of run method for exception handling purposes.
        '''
        new_config = self._readConfig()
        if not self._config:
            self._config = new_config

        self._checkForZooKeeperChanges(new_config)
        provider_manager.ProviderManager.reconfigure(self._config, new_config,
                                                     self._zk,
                                                     only_image_manager=True)
        self._config = new_config

        self._cleanup()


class BuildWorker(BaseWorker):
    def __init__(self, name, builder_id, config_path, secure_path,
                 interval, zk):
        super(BuildWorker, self).__init__(builder_id, config_path, secure_path,
                                          interval, zk)
        self.log = logging.getLogger("nodepool.builder.BuildWorker.%s" % name)
        self.name = 'BuildWorker.%s' % name

    def _getBuildLogRoot(self, name):
        log_dir = self._config.build_log_dir
        if not log_dir:
            log_dir = '/var/log/nodepool/builds'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    def _pruneBuildLogs(self, name):
        if self._config.build_log_retention < 0:
            return
        log_dir = self._getBuildLogRoot(name)
        keep = max(self._config.build_log_retention, 1)
        existing = sorted(os.listdir(log_dir))
        existing = [f for f in existing if f.startswith(name)]
        delete = existing[:0 - keep]
        for f in delete:
            fp = os.path.join(log_dir, f)
            self.log.info("Deleting old build log %s" % (fp,))
            os.unlink(fp)

    def _getBuildLog(self, name, build_id):
        log_dir = self._getBuildLogRoot(name)
        return os.path.join(log_dir, '%s-%s.log' % (name, build_id))

    def _checkForScheduledImageUpdates(self):
        '''
        Check every DIB image to see if it has aged out and needs rebuilt.
        '''
        for diskimage in self._config.diskimages.values():
            # Check if we've been told to shutdown
            # or if ZK connection is suspended
            if not self._running or self._zk.suspended or self._zk.lost:
                return
            try:
                new_config = self._readConfig()
                if new_config != self._config:
                    # If our config isn't up to date then return and start
                    # over with a new config load.
                    return
                self._checkImageForScheduledImageUpdates(diskimage)
            except Exception:
                self.log.exception("Exception checking for scheduled "
                                   "update of diskimage %s",
                                   diskimage.name)

    def _checkImageForScheduledImageUpdates(self, diskimage):
        '''
        Check one DIB image to see if it needs to be rebuilt.

        .. note:: It's important to lock the image build before we check
            the state time and then build to eliminate any race condition.
        '''
        # Check if diskimage builds are paused.
        if diskimage.pause:
            return
        if self._zk.getImagePaused(diskimage.name):
            return

        if not diskimage.image_types:
            # We don't know what formats to build.
            return

        now = int(time.time())
        builds = self._zk.getMostRecentBuilds(1, diskimage.name, zk.READY)

        # If there is no build for this image, or it has aged out
        # or if the current build is missing an image type from
        # the config file, start a new build.
        if (not builds
            or (now - builds[0].state_time) >= diskimage.rebuild_age
            or not set(builds[0].formats).issuperset(diskimage.image_types)
            ):

            try:
                with self._zk.imageBuildLock(diskimage.name, blocking=False):
                    # To avoid locking each image repeatedly, we have an
                    # second, redundant check here to verify that a new
                    # build didn't appear between the first check and the
                    # lock acquisition. If it's not the same build as
                    # identified in the first check above, assume another
                    # BuildWorker created the build for us and continue.
                    builds2 = self._zk.getMostRecentBuilds(
                        1, diskimage.name, zk.READY)
                    if builds2 and builds[0].id != builds2[0].id:
                        return

                    self.log.info("Building image %s" % diskimage.name)
                    self._buildWrapper(diskimage)
            except exceptions.ZKLockException:
                # Lock is already held. Skip it.
                pass

    def _buildWrapper(self, diskimage):
        '''
        Wraps logic for disk image building and ZooKeeper recording.

        :returns: The updated ImageBuild data structure.
        '''
        data = zk.ImageBuild()
        data.state = zk.BUILDING
        data.builder_id = self._builder_id
        data.builder = self._hostname
        data.formats = list(diskimage.image_types)

        bnum = self._zk.storeBuild(diskimage.name, data)

        try:
            data = self._buildImage(bnum, diskimage)
        except Exception:
            # If something unexpected happens, make sure we clean up any
            # build cruft by executing the fallthrough below.
            self.log.exception("Image build failure for build %s of image %s:",
                               bnum, diskimage.name)
            data.state = zk.FAILED

        # If we lost the session during the long running build, this means
        # we've lost our lock and the node was possibly cleaned up during the
        # long build time because state was BUILDING and unlocked. And because
        # the cleanup likely did not get the in-progress dib build files, we
        # need to make sure we get the rest here.
        try:
            self._zk.storeBuild(diskimage.name, data, bnum)
        except Exception:
            # If it disappeared, or the save otherwise failed, cleanup the
            # leaked build manually.
            self.log.exception(
                "Unable to update record for build %s of image %s:",
                bnum, diskimage.name)
            data.id = bnum
            CleanupWorker.deleteLocalBuild(
                self._config.images_dir, diskimage.name, data, self.log)
            data.state = zk.FAILED
            return data

        return self._zk.getBuild(diskimage.name, bnum)

    def _checkForManualBuildRequest(self):
        '''
        Query ZooKeeper for any manual image build requests.
        '''
        for diskimage in self._config.diskimages.values():
            # Check if we've been told to shutdown
            # or if ZK connection is suspended
            if not self._running or self._zk.suspended or self._zk.lost:
                return
            try:
                new_config = self._readConfig()
                if new_config != self._config:
                    # If our config isn't up to date then return and start
                    # over with a new config load.
                    return
                self._checkImageForManualBuildRequest(diskimage)
            except Exception:
                self.log.exception("Exception checking for manual "
                                   "update of diskimage %s",
                                   diskimage)

    def _checkImageForManualBuildRequest(self, diskimage):
        '''
        Query ZooKeeper for a manual image build request for one image.
        '''
        # Check if diskimage builds are paused.
        if diskimage.pause:
            return
        if self._zk.getImagePaused(diskimage.name):
            return

        if not diskimage.image_types:
            # We don't know what formats to build.
            return

        # Reduce use of locks by adding an initial check here and
        # a redundant check after lock acquisition.
        if not self._zk.hasBuildRequest(diskimage.name):
            return

        try:
            with self._zk.imageBuildLock(diskimage.name, blocking=False):
                # Redundant check
                if not self._zk.hasBuildRequest(diskimage.name):
                    return

                self.log.info(
                    "Manual build request for image %s" % diskimage.name)
                data = self._buildWrapper(diskimage)

                # Remove request on a successful build
                if data and data.state == zk.READY:
                    self._zk.removeBuildRequest(diskimage.name)

        except exceptions.ZKLockException:
            # Lock is already held. Skip it.
            pass

    def _buildImage(self, build_id, diskimage):
        '''
        Run the external command to build the diskimage.

        :param str build_id: The ID for the build (used in image filename).
        :param diskimage: The diskimage as retrieved from our config file.

        :returns: An ImageBuild object of build-related data.

        :raises: BuilderError if we failed to execute the build command.
        '''
        base = "-".join([diskimage.name, build_id])
        image_file = DibImageFile(base)
        filename = image_file.to_path(self._config.images_dir, False)

        env = os.environ.copy()
        env['DIB_RELEASE'] = diskimage.release
        env['DIB_IMAGE_NAME'] = diskimage.name
        env['DIB_IMAGE_FILENAME'] = filename

        # Note we use a reference to the nodepool config here so
        # that whenever the config is updated we get up to date
        # values in this thread.
        if self._config.elements_dir:
            env['ELEMENTS_PATH'] = self._config.elements_dir

        # send additional env vars if needed
        for k, v in diskimage.env_vars.items():
            env[k] = v

        img_elements = diskimage.elements
        img_types = ",".join(diskimage.image_types)

        qemu_img_options = ''
        if 'qcow2' in img_types:
            qemu_img_options = DEFAULT_QEMU_IMAGE_COMPAT_OPTIONS

        # A bit of a hack, but useful for CI to pick up the
        # fake-image-create relative to this file easily
        dib_cmd = diskimage.dib_cmd.replace("%p", os.path.dirname(__file__))

        cmd = ('%s -x -t %s --checksum --no-tmpfs %s -o %s %s' %
               (dib_cmd, img_types, qemu_img_options,
                filename, img_elements))

        self._pruneBuildLogs(diskimage.name)
        log_fn = self._getBuildLog(diskimage.name, build_id)

        self.log.info('Running %s' % (cmd,))
        self.log.info('Logging to %s' % (log_fn,))

        start_time = time.monotonic()

        try:
            p = subprocess.Popen(
                shlex.split(cmd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                env=env)
        except OSError as e:
            raise exceptions.BuilderError(
                "Failed to exec '%s'. Error: '%s'" % (cmd, e.strerror)
            )

        # Make subprocess stdout non-blocking
        fd = p.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # Poll subprocess stdout for readability
        r, w, e = select.select([fd], [], [], 0)
        bitmask = (select.POLLIN | select.POLLHUP)
        poll = select.poll()
        poll.register(fd, bitmask)

        rc = None
        did_timeout = False
        subprocess_done = False

        def buildDidTimeout():
            build_time = time.monotonic() - start_time
            if build_time > diskimage.build_timeout:
                return True
            return False

        with open(log_fn, 'wb') as log:

            # While the subprocess is running, we will loop through stdout
            # events. If we can read data, write that out to the log file.
            # If the subprocess completes, set the flag so we can exit and
            # write the return code.
            #
            # We check for build timeouts in two places: after we have read
            # all available data in the buffer (which will cause an early exit
            # of the poll loop), and after a poll timeout. If we did not have
            # a check after the reads, we would have to have a poll timeout
            # to occur to check for a build timeout, which may not happen if
            # there is constantly data available for reading.

            while not subprocess_done:
                for fd, event in poll.poll(BUILD_PROCESS_POLL_TIMEOUT):

                    # Data available for reading
                    if event & select.POLLIN:
                        data = p.stdout.read(1024)
                        while data:
                            log.write(data)
                            log.flush()
                            data = p.stdout.read(1024)
                        if buildDidTimeout():
                            break

                    # Subprocess complete
                    if event & select.POLLHUP:
                        subprocess_done = True
                        rc = p.wait()

                if not subprocess_done:
                    if buildDidTimeout():
                        did_timeout = True
                        rc = 1
                        self.log.error(
                            "Build timeout for image %s, build %s (log: %s)",
                            diskimage.name, build_id, log_fn)
                        p.kill()
                        break

            # Subprocess finished, write return code
            if not did_timeout:
                m = "Exit code: %s\n" % rc
                log.write(m.encode('utf8'))

        # It's possible the connection to the ZK cluster could have been
        # interrupted during the build. If so, wait for it to return.
        # It could transition directly from SUSPENDED to CONNECTED, or go
        # through the LOST state before CONNECTED.
        did_suspend = False
        while self._zk.suspended or self._zk.lost:
            did_suspend = True
            self.log.info("ZooKeeper suspended during build. Waiting")
            time.sleep(SUSPEND_WAIT_TIME)
        if did_suspend:
            self.log.info("ZooKeeper available. Resuming")

        build_time = time.monotonic() - start_time

        build_data = zk.ImageBuild()
        build_data.builder_id = self._builder_id
        build_data.builder = self._hostname
        build_data.username = diskimage.username
        build_data.python_path = diskimage.python_path
        build_data.shell_type = diskimage.shell_type

        if self._statsd:
            pipeline = self._statsd.pipeline()

        if self._zk.didLoseConnection:
            self.log.info("ZooKeeper lost while building %s" % diskimage.name)
            self._zk.resetLostFlag()
            build_data.state = zk.FAILED
        elif p.returncode or did_timeout:
            self.log.info(
                "DIB failed creating %s (%s) (timeout=%s)" % (
                    diskimage.name, p.returncode, did_timeout))
            build_data.state = zk.FAILED
        else:
            self.log.info("DIB image %s is built" % diskimage.name)
            build_data.state = zk.READY
            build_data.formats = list(diskimage.image_types)

            if self._statsd:
                # record stats on the size of each image we create
                for ext in img_types.split(','):
                    key = 'nodepool.dib_image_build.%s.%s.size' % (
                        diskimage.name, ext)
                    # A bit tricky because these image files may be sparse
                    # files; we only want the true size of the file for
                    # purposes of watching if we've added too much stuff
                    # into the image.  Note that st_blocks is defined as
                    # 512-byte blocks by stat(2)
                    size = os.stat("%s.%s" % (filename, ext)).st_blocks * 512
                    self.log.debug("%s created image %s.%s (size: %d) " %
                                   (diskimage.name, filename, ext, size))
                    pipeline.gauge(key, size)

        if self._statsd:
            # report result to statsd
            key_base = 'nodepool.dib_image_build.%s.status' % (
                diskimage.name)
            pipeline.timing(key_base + '.duration',
                            int(build_time * 1000))
            pipeline.gauge(key_base + '.rc', rc)
            pipeline.gauge(key_base + '.last_build',
                           int(time.time()))
            pipeline.send()

        return build_data

    def run(self):
        '''
        Start point for the BuildWorker thread.
        '''
        self._running = True
        while self._running:
            # Don't do work if we've lost communication with the ZK cluster
            did_suspend = False
            while self._zk and (self._zk.suspended or self._zk.lost):
                did_suspend = True
                self.log.info("ZooKeeper suspended. Waiting")
                time.sleep(SUSPEND_WAIT_TIME)
            if did_suspend:
                self.log.info("ZooKeeper available. Resuming")

            try:
                self._run()
            except Exception:
                self.log.exception("Exception in BuildWorker:")
                time.sleep(10)

            self._stop_event.wait(self._interval)

    def _run(self):
        '''
        Body of run method for exception handling purposes.
        '''
        # NOTE: For the first iteration, we expect self._config to be None
        new_config = self._readConfig()
        if not self._config:
            self._config = new_config

        self._checkForZooKeeperChanges(new_config)
        self._config = new_config
        self._checkForScheduledImageUpdates()
        self._checkForManualBuildRequest()


class UploadWorker(BaseWorker):
    def __init__(self, name, builder_id, config_path, secure_path,
                 interval, zk):
        super(UploadWorker, self).__init__(builder_id, config_path,
                                           secure_path, interval, zk)
        self.log = logging.getLogger("nodepool.builder.UploadWorker.%s" % name)
        self.name = 'UploadWorker.%s' % name

    def _reloadConfig(self):
        '''
        Reload the nodepool configuration file.
        '''
        new_config = self._readConfig()
        if not self._config:
            self._config = new_config

        self._checkForZooKeeperChanges(new_config)
        provider_manager.ProviderManager.reconfigure(self._config, new_config,
                                                     self._zk,
                                                     only_image_manager=True)
        self._config = new_config

    def _uploadImage(self, build_id, upload_id, image_name, images, provider,
                     username, python_path, shell_type):
        '''
        Upload a local DIB image build to a provider.

        :param str build_id: Unique ID of the image build to upload.
        :param str upload_id: Unique ID of the upload.
        :param str image_name: Name of the diskimage.
        :param list images: A list of DibImageFile objects from this build
            that available for uploading.
        :param provider: The provider from the parsed config file.
        :param username:
        :param python_path:
        :param shell_type:
        '''
        start_time = time.time()
        timestamp = int(start_time)

        image = None
        for i in images:
            if provider.image_type == i.extension:
                image = i
                break

        if not image:
            raise exceptions.BuilderInvalidCommandError(
                "Unable to find image file of type %s for id %s to upload" %
                (provider.image_type, build_id)
            )

        self.log.debug("Found image file of type %s for image id: %s" %
                       (image.extension, image.image_id))

        filename = image.to_path(self._config.images_dir, with_extension=True)

        ext_image_name = provider.image_name_format.format(
            image_name=image_name, timestamp=str(timestamp)
        )

        self.log.info("Uploading DIB image build %s from %s to %s" %
                      (build_id, filename, provider.name))

        manager = self._config.provider_managers[provider.name]
        provider_image = provider.diskimages.get(image_name)
        if provider_image is None:
            raise exceptions.BuilderInvalidCommandError(
                "Could not find matching provider image for %s" % image_name
            )

        meta = provider_image.meta.copy()
        meta['nodepool_build_id'] = build_id
        meta['nodepool_upload_id'] = upload_id

        try:
            external_id = manager.uploadImage(
                ext_image_name, filename,
                image_type=image.extension,
                meta=meta,
                md5=image.md5,
                sha256=image.sha256,
            )
        except Exception:
            self.log.exception(
                "Failed to upload build %s of image %s to provider %s" %
                (build_id, image_name, provider.name))
            data = zk.ImageUpload()
            data.state = zk.FAILED
            return data

        if provider.post_upload_hook:
            try:
                cmd = [
                    provider.post_upload_hook,
                    provider.name,
                    external_id,
                    filename
                ]
                self.log.info('Running post upload hook %s', cmd)
                p = subprocess.run(cmd, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, check=True)
            except Exception as e:
                if isinstance(e, subprocess.CalledProcessError):
                    self.log.error('Post upload hook failed with '
                                   'exit code %s\nstdout:\n%s\nstderr:\n%s',
                                   e.returncode, e.stdout.decode(),
                                   e.stderr.decode())
                else:
                    self.log.exception('Unknown exception during upload hook')

                try:
                    manager.deleteImage(ext_image_name)
                except Exception:
                    # Image delete failed but we cannot do anything about this
                    # right now so just log the exception.
                    self.log.exception('Unable to delete image "%s"',
                                       ext_image_name)
                data = zk.ImageUpload()
                data.state = zk.FAILED
                return data

            self.log.info(
                'Post upload hook success with exit code %s\n'
                'stdout:\n%s\nstderr:\n%s',
                p.returncode, p.stdout.decode(), p.stderr.decode())

        if self._statsd:
            dt = int((time.time() - start_time) * 1000)
            key = 'nodepool.image_update.%s.%s' % (image_name,
                                                   provider.name)
            self._statsd.timing(key, dt)
            self._statsd.incr(key)

        base = "-".join([image_name, build_id])
        self.log.info("Image build %s (external_id %s) in %s is ready" %
                      (base, external_id, provider.name))

        data = zk.ImageUpload()
        data.state = zk.READY
        data.external_id = external_id
        data.external_name = ext_image_name
        data.format = image.extension
        data.username = username
        data.python_path = python_path
        data.shell_type = shell_type

        return data

    def _checkForProviderUploads(self):
        '''
        Check for any image builds that need to be uploaded to providers.

        If we find any builds in the 'ready' state that haven't been uploaded
        to providers, do the upload if they are available on the local disk.
        '''
        for provider in self._config.providers.values():
            if not provider.manage_images:
                continue
            for image in provider.diskimages.values():
                uploaded = False

                # Check if we've been told to shutdown
                # or if ZK connection is suspended
                if not self._running or self._zk.suspended or self._zk.lost:
                    return
                try:
                    uploaded = self._checkProviderImageUpload(provider, image)
                except Exception:
                    self.log.exception("Error uploading image %s "
                                       "to provider %s:",
                                       image.name, provider.name)

                # NOTE: Due to the configuration file disagreement issue
                # (the copy we have may not be current), if we took the time
                # to attempt to upload an image, let's short-circuit this loop
                # to give us a chance to reload the configuration file.
                if uploaded:
                    return

    def _checkProviderImageUpload(self, provider, image):
        '''
        The main body of _checkForProviderUploads.  This encapsulates
        checking whether an image for a provider should be uploaded
        and performing the upload.  It is a separate function so that
        exception handling can treat all provider-image uploads
        indepedently.

        :returns: True if an upload was attempted, False otherwise.
        '''
        # Check if image uploads are paused.
        if provider.diskimages.get(image.name).pause:
            return False

        # Search for the most recent 'ready' image build
        builds = self._zk.getMostRecentBuilds(1, image.name,
                                              zk.READY)
        if not builds:
            return False

        build = builds[0]

        # Search for locally built images. The image name and build
        # sequence ID is used to name the image.
        local_images = DibImageFile.from_image_id(
            self._config.images_dir, "-".join([image.name, build.id]))
        if not local_images:
            return False

        # See if this image has already been uploaded
        upload = self._zk.getMostRecentBuildImageUploads(
            1, image.name, build.id, provider.name, zk.READY)
        if upload:
            return False

        # See if this provider supports the available image formats
        if provider.image_type not in build.formats:
            return False

        try:
            with self._zk.imageUploadLock(
                image.name, build.id, provider.name,
                blocking=False
            ):
                # Verify once more that it hasn't been uploaded since the
                # last check.
                upload = self._zk.getMostRecentBuildImageUploads(
                    1, image.name, build.id, provider.name, zk.READY)
                if upload:
                    return False

                # NOTE: Due to the configuration file disagreement issue
                # (the copy we have may not be current), we try to verify
                # that another thread isn't trying to delete this build just
                # before we upload.
                b = self._zk.getBuild(image.name, build.id)
                if not b or b.state == zk.DELETING:
                    return False

                # New upload number with initial state 'uploading'
                data = zk.ImageUpload()
                data.state = zk.UPLOADING
                data.username = build.username
                data.python_path = build.python_path
                data.shell_type = build.shell_type

                upnum = self._zk.storeImageUpload(
                    image.name, build.id, provider.name, data)

                data = self._uploadImage(build.id, upnum, image.name,
                                         local_images, provider,
                                         build.username, build.python_path,
                                         build.shell_type)

                # Set final state
                self._zk.storeImageUpload(image.name, build.id,
                                          provider.name, data, upnum)
                return True
        except exceptions.ZKLockException:
            # Lock is already held. Skip it.
            return False

    def run(self):

        '''
        Start point for the UploadWorker thread.
        '''
        self._running = True
        while self._running:
            # Don't do work if we've lost communication with the ZK cluster
            did_suspend = False
            while self._zk and (self._zk.suspended or self._zk.lost):
                did_suspend = True
                self.log.info("ZooKeeper suspended. Waiting")
                time.sleep(SUSPEND_WAIT_TIME)
            if did_suspend:
                self.log.info("ZooKeeper available. Resuming")

            try:
                self._reloadConfig()
                self._checkForProviderUploads()
            except Exception:
                self.log.exception("Exception in UploadWorker:")
                time.sleep(10)

            self._stop_event.wait(self._interval)

        provider_manager.ProviderManager.stopProviders(self._config)


class NodePoolBuilder(object):
    '''
    Main class for the Nodepool Builder.

    The builder has the responsibility to:

        * Start and maintain the working state of each worker thread.
    '''
    log = logging.getLogger("nodepool.builder.NodePoolBuilder")

    def __init__(self, config_path, secure_path=None,
                 num_builders=1, num_uploaders=4):
        '''
        Initialize the NodePoolBuilder object.

        :param str config_path: Path to configuration file.
        :param str secure_path: Path to secure configuration file.
        :param int num_builders: Number of build workers to start.
        :param int num_uploaders: Number of upload workers to start.
        '''
        self._config_path = config_path
        self._secure_path = secure_path
        self._config = None
        self._num_builders = num_builders
        self._build_workers = []
        self._num_uploaders = num_uploaders
        self._upload_workers = []
        self._janitor = None
        self._running = False
        self.cleanup_interval = 60
        self.build_interval = 10
        self.upload_interval = 10
        self.zk = None

        # This lock is needed because the run() method is started in a
        # separate thread of control, which can return before the scheduler
        # has completed startup. We need to avoid shutting down before the
        # startup process has completed.
        self._start_lock = threading.Lock()

    # ======================================================================
    # Private methods
    # ======================================================================

    def _getBuilderID(self, id_file):
        if not os.path.exists(id_file):
            with open(id_file, "w") as f:
                builder_id = str(uuid.uuid4())
                f.write(builder_id)
            return builder_id

        with open(id_file, "r") as f:
            builder_id = f.read()
        return builder_id

    def _getAndValidateConfig(self):
        config = nodepool_config.loadConfig(self._config_path)
        if self._secure_path:
            nodepool_config.loadSecureConfig(config, self._secure_path)
        if not config.zookeeper_servers.values():
            raise RuntimeError('No ZooKeeper servers specified in config.')
        if not config.images_dir:
            raise RuntimeError('No images-dir specified in config.')
        return config

    # ======================================================================
    # Public methods
    # ======================================================================

    def start(self):
        '''
        Start the builder.

        The builder functionality is encapsulated within threads run
        by the NodePoolBuilder. This starts the needed sub-threads
        which will run forever until we tell them to stop.
        '''
        with self._start_lock:
            if self._running:
                raise exceptions.BuilderError('Cannot start, already running.')

            self._config = self._getAndValidateConfig()
            self._running = True

            builder_id_file = os.path.join(self._config.images_dir,
                                           "builder_id.txt")
            builder_id = self._getBuilderID(builder_id_file)

            # All worker threads share a single ZooKeeper instance/connection.
            self.zk = zk.ZooKeeper(enable_cache=False)
            self.zk.connect(
                list(self._config.zookeeper_servers.values()),
                tls_cert=self._config.zookeeper_tls_cert,
                tls_key=self._config.zookeeper_tls_key,
                tls_ca=self._config.zookeeper_tls_ca)

            self.log.debug('Starting listener for build jobs')

            # Create build and upload worker objects
            for i in range(self._num_builders):
                w = BuildWorker(i, builder_id,
                                self._config_path, self._secure_path,
                                self.build_interval, self.zk)
                w.start()
                self._build_workers.append(w)

            for i in range(self._num_uploaders):
                w = UploadWorker(i, builder_id,
                                 self._config_path, self._secure_path,
                                 self.upload_interval, self.zk)
                w.start()
                self._upload_workers.append(w)

            if self.cleanup_interval > 0:
                self._janitor = CleanupWorker(
                    0, builder_id,
                    self._config_path, self._secure_path,
                    self.cleanup_interval, self.zk)
                self._janitor.start()

            # Wait until all threads are running. Otherwise, we have a race
            # on the worker _running attribute if shutdown() is called before
            # run() actually begins.
            workers = self._build_workers + self._upload_workers
            if self._janitor:
                workers += [self._janitor]
            while not all([
                x.running for x in (workers)]):
                time.sleep(0)

    def stop(self):
        '''
        Stop the builder.

        Signal the sub threads to begin the shutdown process. We don't
        want this method to return until the scheduler has successfully
        stopped all of its own threads.
        '''
        with self._start_lock:
            self.log.debug("Stopping. NodePoolBuilder shutting down workers")
            # Note we do not add the upload workers to this list intentionally.
            # The reason for this is that uploads can take many hours and there
            # is no good way to stop the blocking writes performed by the
            # uploads in order to join() below on a reasonable amount of time.
            # Killing the process will stop the upload then both the record
            # in zk and in the cloud will be deleted by any other running
            # builders or when this builder starts again.
            workers = self._build_workers
            if self._janitor:
                workers += [self._janitor]
            for worker in (workers):
                worker.shutdown()

        self._running = False

        self.log.debug('Waiting for jobs to complete')

        # Do not exit until all of our owned threads exit.
        for worker in (workers):
            worker.join()

        self.log.debug('Stopping providers')
        provider_manager.ProviderManager.stopProviders(self._config)

        self.log.debug('Terminating ZooKeeper connection')
        self.zk.disconnect()

        self.log.debug('Finished stopping')
