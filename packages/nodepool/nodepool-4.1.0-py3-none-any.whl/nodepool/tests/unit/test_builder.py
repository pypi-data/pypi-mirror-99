# Copyright (C) 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import uuid
import fixtures
import mock
import time

from pathlib import Path

from nodepool import builder, exceptions, tests
from nodepool.driver.fake import provider as fakeprovider
from nodepool import zk
from nodepool.config import Config
from nodepool.nodeutils import iterate_timeout


class TestNodepoolBuilderDibImage(tests.BaseTestCase):
    def test_from_path(self):
        image = builder.DibImageFile.from_path(
            '/foo/bar/myid1234.qcow2')
        self.assertEqual(image.image_id, 'myid1234')
        self.assertEqual(image.extension, 'qcow2')

    def test_from_path_with_Path(self):
        image = builder.DibImageFile.from_path(
            Path('/foo/bar/myid1234.qcow2'))
        self.assertEqual(image.image_id, 'myid1234')
        self.assertEqual(image.extension, 'qcow2')

    def test_from_image_id(self):
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        image_path = os.path.join(tempdir.path, 'myid1234.qcow2')
        open(image_path, 'w')

        images = builder.DibImageFile.from_image_id(tempdir.path, 'myid1234')
        self.assertEqual(len(images), 1)

        image = images[0]
        self.assertEqual(image.image_id, 'myid1234')
        self.assertEqual(image.extension, 'qcow2')

    def test_from_id_multiple(self):
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        image_path_1 = os.path.join(tempdir.path, 'myid1234.qcow2')
        image_path_2 = os.path.join(tempdir.path, 'myid1234.raw')
        open(image_path_1, 'w')
        open(image_path_2, 'w')

        images = builder.DibImageFile.from_image_id(tempdir.path, 'myid1234')
        images = sorted(images, key=lambda x: x.extension)
        self.assertEqual(len(images), 2)

        self.assertEqual(images[0].extension, 'qcow2')
        self.assertEqual(images[1].extension, 'raw')

    def test_from_images_dir(self):
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        image_path_1 = os.path.join(tempdir.path, 'myid1234.qcow2')
        image_path_2 = os.path.join(tempdir.path, 'myid1234.raw')
        open(image_path_1, 'w')
        open(image_path_2, 'w')

        images = builder.DibImageFile.from_images_dir(tempdir.path)
        images = sorted(images, key=lambda x: x.extension)
        self.assertEqual(len(images), 2)

        self.assertEqual(images[0].image_id, 'myid1234')
        self.assertEqual(images[0].extension, 'qcow2')
        self.assertEqual(images[1].image_id, 'myid1234')
        self.assertEqual(images[1].extension, 'raw')

    def test_to_path(self):
        image = builder.DibImageFile('myid1234', 'qcow2')
        self.assertEqual(image.to_path('/imagedir'),
                         '/imagedir/myid1234.qcow2')
        self.assertEqual(image.to_path('/imagedir/'),
                         '/imagedir/myid1234.qcow2')
        self.assertEqual(image.to_path('/imagedir/', False),
                         '/imagedir/myid1234')

        image = builder.DibImageFile('myid1234')
        self.assertRaises(exceptions.BuilderError, image.to_path, '/imagedir/')


class TestNodepoolBuilderImageInheritance(tests.BaseTestCase):
    def test_parent_job(self):
        config = Config()
        diskimages = [
            {
                'name': 'parent',
                'dib-cmd': 'parent-dib-cmd',
                'elements': ['a', 'b'],
                'env-vars': {
                    'A': 'foo',
                    'B': 'bar',
                },
                'release': 21,
            },
            {
                'name': 'child',
                'parent': 'parent',
                'dib-cmd': 'override-dib-cmd',
                'elements': ['c'],
                'env-vars': {
                    'A': 'override_foo',
                    'C': 'moo'
                },
            },

        ]
        config.setDiskImages(diskimages)
        parsed = config.diskimages['child']
        self.assertEqual(parsed.dib_cmd, 'override-dib-cmd')
        self.assertEqual(parsed.release, '21')
        self.assertEqual(parsed.elements, 'a b c')
        self.assertDictEqual({
            'A': 'override_foo',
            'B': 'bar',
            'C': 'moo',
        }, parsed.env_vars)

    def test_abstract_jobs(self):
        config = Config()
        diskimages = [
            {
                'name': 'abstract',
                'abstract': True,
                'elements': ['a', 'b'],
                'env-vars': {
                    'A': 'foo',
                    'B': 'bar',
                },
            },
            {
                'name': 'another-abstract',
                'abstract': True,
                'parent': 'abstract',
                'elements': ['c'],
                'env-vars': {
                    'A': 'override_abstract',
                    'C': 'moo'
                },
            },
            {
                'name': 'job',
                'parent': 'another-abstract',
                'elements': ['d'],
                'dib-cmd': 'override-dib-cmd',
                'env-vars': {
                    'A': 'override_foo_again',
                    'D': 'zoo'
                },
            },

        ]
        config.setDiskImages(diskimages)
        parsed = config.diskimages['job']
        self.assertEqual(parsed.dib_cmd, 'override-dib-cmd')
        self.assertEqual(parsed.elements, 'a b c d')
        self.assertDictEqual({
            'A': 'override_foo_again',
            'B': 'bar',
            'C': 'moo',
            'D': 'zoo',
        }, parsed.env_vars)


class TestNodePoolBuilder(tests.DBTestCase):

    def test_start_stop(self):
        config = self.setup_config('node.yaml')
        nb = builder.NodePoolBuilder(config)
        nb.cleanup_interval = .5
        nb.build_interval = .1
        nb.upload_interval = .1
        nb.start()
        nb.stop()

    def test_builder_id_file(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        path = os.path.join(self._config_images_dir.path, 'builder_id.txt')

        # Validate the unique ID file exists and contents are what we expect
        self.assertTrue(os.path.exists(path))
        with open(path, "r") as f:
            the_id = f.read()
            obj = uuid.UUID(the_id, version=4)
            self.assertEqual(the_id, str(obj))

    def test_image_upload_fail(self):
        """Test that image upload fails are handled properly."""

        # Now swap out the upload fake so that the next uploads fail
        fake_client = fakeprovider.FakeUploadFailCloud(times_to_fail=1)

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeprovider.FakeProvider, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        # NOTE(pabelanger): Disable CleanupWorker thread for nodepool-builder
        # as we currently race it to validate our failed uploads.
        self.useBuilder(configfile, cleanup_interval=0)
        pool.start()
        self.waitForImage('fake-provider', 'fake-image')
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        newest_builds = self.zk.getMostRecentBuilds(1, 'fake-image',
                                                    state=zk.READY)
        self.assertEqual(1, len(newest_builds))

        uploads = self.zk.getUploads('fake-image', newest_builds[0].id,
                                     'fake-provider', states=[zk.FAILED])
        self.assertEqual(1, len(uploads))

    def test_provider_addition(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_provider.yaml')
        self.waitForImage('fake-provider2', 'fake-image')

    def test_provider_removal(self):
        configfile = self.setup_config('node_two_provider.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        image = self.zk.getMostRecentImageUpload('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_provider_remove.yaml')
        self.waitForImageDeletion('fake-provider2', 'fake-image')
        image2 = self.zk.getMostRecentImageUpload('fake-provider',
                                                  'fake-image')
        self.assertEqual(image, image2)

    def test_image_addition(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_image.yaml')
        self.waitForImage('fake-provider', 'fake-image2')

    def test_image_removal(self):
        configfile = self.setup_config('node_two_image.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider', 'fake-image2')
        self.replace_config(configfile, 'node_two_image_remove.yaml')
        self.waitForImageDeletion('fake-provider', 'fake-image2')
        self.waitForBuildDeletion('fake-image2', '0000000001')

    def test_image_removal_dib_deletes_first(self):
        # Break cloud image deleting
        fake_client = fakeprovider.FakeDeleteImageFailCloud()

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeprovider.FakeProvider, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_two_image.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        img = self.waitForImage('fake-provider', 'fake-image2')

        # Ask nodepool to delete the image build and uploads
        self.replace_config(configfile, 'node_two_image_remove.yaml')
        # Wait for image files on disk to be deleted.
        for _ in iterate_timeout(10, Exception,
                                 'DIB disk files did not delete first'):
            self.wait_for_threads()
            files = builder.DibImageFile.from_image_id(
                self._config_images_dir.path, 'fake-image2-0000000001')
            if not files:
                break
        # Check image is still in fake-provider cloud
        img.state = zk.DELETING
        self.assertEqual(
            self.zk.getImageUpload('fake-image2', '0000000001',
                                   'fake-provider', '0000000001'),
            img)

        # Release things by unbreaking image deleting. This allows cloud
        # and zk records to be removed.
        fake_client._fail = False
        # Check image is removed from cloud and zk
        self.waitForImageDeletion('fake-provider', 'fake-image2', match=img)
        # Check build is removed from zk
        self.waitForBuildDeletion('fake-image2', '0000000001')

    def test_image_rebuild_age(self):
        self._test_image_rebuild_age()

    def _test_image_rebuild_age(self, expire=86400):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        build = self.waitForBuild('fake-image', '0000000001')
        log_path1 = os.path.join(self._config_build_log_dir.path,
                                 'fake-image-0000000001.log')
        self.assertTrue(os.path.exists(log_path1))
        image = self.waitForImage('fake-provider', 'fake-image')
        # Expire rebuild-age (default: 1day) to force a new build.
        build.state_time -= expire
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build, '0000000001')
        self.waitForBuild('fake-image', '0000000002')
        log_path2 = os.path.join(self._config_build_log_dir.path,
                                 'fake-image-0000000002.log')
        self.assertTrue(os.path.exists(log_path2))
        self.waitForImage('fake-provider', 'fake-image', [image])
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)
        return (build, image)

    def test_image_rotation(self):
        # Expire rebuild-age (2days), to avoid problems when expiring 2 images.
        self._test_image_rebuild_age(expire=172800)
        build = self.waitForBuild('fake-image', '0000000002')
        # Expire rebuild-age (default: 1day) to force a new build.
        build.state_time -= 86400
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build, '0000000002')
        self.waitForBuildDeletion('fake-image', '0000000001')
        self.waitForBuild('fake-image', '0000000003')
        log_path1 = os.path.join(self._config_build_log_dir.path,
                                 'fake-image-0000000001.log')
        log_path2 = os.path.join(self._config_build_log_dir.path,
                                 'fake-image-0000000002.log')
        log_path3 = os.path.join(self._config_build_log_dir.path,
                                 'fake-image-0000000003.log')
        # Our log retention is set to 1, so the first log should be deleted.
        self.assertFalse(os.path.exists(log_path1))
        self.assertTrue(os.path.exists(log_path2))
        self.assertTrue(os.path.exists(log_path3))
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)

    def test_image_rotation_invalid_external_name(self):
        # NOTE(pabelanger): We are forcing fake-image to leak in fake-provider.
        # We do this to test our CleanupWorker will properly delete diskimage
        # builds from the HDD. For this test, we don't care about the leaked
        # image.
        #
        # Ensure we have a total of 3 diskimages on disk, so we can confirm
        # nodepool-builder will properly purge the 1 diskimage build leaving a
        # total of 2 diskimages on disk at all times.

        # Expire rebuild-age (2days), to avoid problems when expiring 2 images.
        build001, image001 = self._test_image_rebuild_age(expire=172800)
        build002 = self.waitForBuild('fake-image', '0000000002')

        # Make sure 2rd diskimage build was uploaded.
        image002 = self.waitForImage('fake-provider', 'fake-image', [image001])
        self.assertEqual(image002.build_id, '0000000002')

        # Delete external name / id so we can test exception handlers.
        upload = self.zk.getUploads(
            'fake-image', '0000000001', 'fake-provider', zk.READY)[0]
        upload.external_name = None
        upload.external_id = None
        with self.zk.imageUploadLock(upload.image_name, upload.build_id,
                                     upload.provider_name, blocking=True,
                                     timeout=1):
            self.zk.storeImageUpload(upload.image_name, upload.build_id,
                                     upload.provider_name, upload, upload.id)

        # Expire rebuild-age (default: 1day) to force a new build.
        build002.state_time -= 86400
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build002, '0000000002')
        self.waitForBuildDeletion('fake-image', '0000000001')

        # Make sure fake-image for fake-provider is removed from zookeeper.
        upload = self.zk.getUploads(
            'fake-image', '0000000001', 'fake-provider')
        self.assertEqual(len(upload), 0)
        self.waitForBuild('fake-image', '0000000003')

        # Ensure we only have 2 builds on disk.
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)

        # Make sure 3rd diskimage build was uploaded.
        image003 = self.waitForImage(
            'fake-provider', 'fake-image', [image001, image002])
        self.assertEqual(image003.build_id, '0000000003')

    def test_cleanup_hard_upload_fails(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        upload = self.zk.getUploads('fake-image', '0000000001',
                                    'fake-provider', zk.READY)[0]

        # Store a new ZK node as UPLOADING to represent a hard fail
        upload.state = zk.UPLOADING

        with self.zk.imageUploadLock(upload.image_name, upload.build_id,
                                     upload.provider_name, blocking=True,
                                     timeout=1):
            upnum = self.zk.storeImageUpload(upload.image_name,
                                             upload.build_id,
                                             upload.provider_name,
                                             upload)

        # Now it should disappear from the current build set of uploads
        self.waitForUploadRecordDeletion(upload.provider_name,
                                         upload.image_name,
                                         upload.build_id,
                                         upnum)

    def test_cleanup_failed_image_build(self):
        configfile = self.setup_config('node_diskimage_fail.yaml')
        self.useBuilder(configfile)
        # Wait for the build to fail before we replace our config. Otherwise
        # we may replace the config before we build the image.
        found = False
        for _ in iterate_timeout(10, Exception, 'image builds to fail', 0.1):
            builds = self.zk.getBuilds('fake-image')
            for build in builds:
                # Lexicographical order
                if build and build.id > '0000000001':
                    # We know we've built more than one image and we know
                    # they have all failed. We can't check if they have
                    # failed directly because they may be cleaned up.
                    found = build.id
                    break
                time.sleep(0.1)
            if found:
                break

        # Now replace the config with a valid config and check that the image
        # builds successfully. Finally check that the failed image is gone.
        self.replace_config(configfile, 'node.yaml')
        self.waitForImage('fake-provider', 'fake-image')
        # Make sure our cleanup worker properly removes the first build.
        self.waitForBuildDeletion('fake-image', found)
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.rc',
                                '127', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.duration', None, 'ms')

    def test_diskimage_build_only(self):
        configfile = self.setup_config('node_diskimage_only.yaml')
        self.useBuilder(configfile)
        build_tar = self.waitForBuild('fake-image', '0000000001')

        self.assertEqual(build_tar._formats, ['tar'])
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.rc',
                                '0', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.duration', None, 'ms')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.tar.size', '4096', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.last_build', None, 'g')

    def test_diskimage_build_formats(self):
        configfile = self.setup_config('node_diskimage_formats.yaml')
        self.useBuilder(configfile)
        build_default = self.waitForBuild('fake-image-default-format',
                                          '0000000001')
        build_vhd = self.waitForBuild('fake-image-vhd', '0000000001')

        self.assertEqual(build_default._formats, ['qcow2'])
        self.assertEqual(build_vhd._formats, ['vhd'])
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image-default-format.qcow2.size',
                                '4096', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image-vhd.vhd.size', '4096', 'g')

    def test_diskimage_build_parents(self):
        configfile = self.setup_config('node_diskimage_parents.yaml')
        self.useBuilder(configfile)
        self.waitForBuild('parent-image-1', '0000000001')
        self.waitForBuild('parent-image-2', '0000000001')

    @mock.patch('select.poll')
    def test_diskimage_build_timeout(self, mock_poll):
        configfile = self.setup_config('diskimage_build_timeout.yaml')
        builder.BUILD_PROCESS_POLL_TIMEOUT = 500
        self.useBuilder(configfile, cleanup_interval=0)
        self.waitForBuild('fake-image', '0000000001', states=(zk.FAILED,))

    def test_session_loss_during_build(self):
        configfile = self.setup_config('node.yaml')

        # We need to make the image build process pause so we can introduce
        # a simulated ZK session loss. The fake dib process will sleep while
        # the pause file is present in the images directory supplied to it.
        pause_file = os.path.join(self._config_images_dir.path,
                                  "fake-image-create.pause")
        open(pause_file, 'w')

        # Disable cleanup thread to verify builder cleans up after itself
        bldr = self.useBuilder(configfile, cleanup_interval=0)
        self.waitForBuild('fake-image', '0000000001', states=(zk.BUILDING,))

        # The build should now be paused just before writing out any DIB files.
        # Mock the next call to storeBuild() which is supposed to be the update
        # of the current build in ZooKeeper. This failure simulates losing the
        # ZK session and not being able to update the record.
        bldr.zk.storeBuild = mock.Mock(side_effect=Exception('oops'))

        # Allow the fake-image-create to continue by removing the pause file
        os.remove(pause_file)

        # The fake dib process writes out a .done file at the end. We need
        # this so we do not continue in this test until *after* all files are
        # written by that dib process.
        done_file = os.path.join(self._config_images_dir.path,
                                 "fake-image-create.done")
        while not os.path.exists(done_file):
            time.sleep(.1)

        # There shouldn't be any DIB files even though cleanup thread is
        # disabled because the builder should clean up after itself.
        images_dir = bldr._config.images_dir

        # Wait for builder to remove the leaked files
        image_files = builder.DibImageFile.from_image_id(
            images_dir, 'fake-image-0000000001')
        while image_files:
            time.sleep(.1)
            image_files = builder.DibImageFile.from_image_id(
                images_dir, 'fake-image-0000000001')

    def test_upload_removal_retries_until_success(self):
        '''
        If removing an image from a provider fails on the first attempt, make
        sure that we retry until successful.

        This test starts with two images uploaded to the provider. It then
        removes one of the images by setting the state to FAILED which should
        begin the process to delete the image from the provider.
        '''
        configfile = self.setup_config('builder_2_diskimages.yaml')
        bldr = self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image1')
        image = self.waitForImage('fake-provider', 'fake-image2')

        # Introduce a failure in the upload deletion process by replacing
        # the cleanup thread's deleteImage() call with one that fails.
        cleanup_thd = bldr._janitor
        cleanup_mgr = cleanup_thd._config.provider_managers['fake-provider']
        saved_method = cleanup_mgr.deleteImage
        cleanup_mgr.deleteImage = mock.Mock(side_effect=Exception('Conflict'))

        # Manually cause the image to be deleted from the provider. Note that
        # we set it to FAILED instead of DELETING because that bypasses the
        # bit of code we want to test here in the CleanupWorker._deleteUpload()
        # method.
        image.state = zk.FAILED
        bldr.zk.storeImageUpload(image.image_name, image.build_id,
                                 image.provider_name, image, image.id)

        # Pick a call count > 1 to verify we make multiple attempts at
        # deleting the image in the provider.
        for _ in iterate_timeout(10, Exception, 'call count to increase'):
            if cleanup_mgr.deleteImage.call_count >= 5:
                break

        # Remove the failure to verify deletion.
        cleanup_mgr.deleteImage = saved_method
        self.waitForUploadRecordDeletion(image.provider_name, image.image_name,
                                         image.build_id, image.id)

    def test_post_upload_hook(self):
        configfile = self.setup_config('node_upload_hook.yaml')
        bldr = self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        images_dir = bldr._config.images_dir
        post_file = os.path.join(
            images_dir, 'fake-image-0000000001.qcow2.post')
        self.assertTrue(os.path.exists(post_file), 'Post hook file exists')
