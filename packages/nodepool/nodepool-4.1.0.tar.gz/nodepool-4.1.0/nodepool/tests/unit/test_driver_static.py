# Copyright (C) 2017 Red Hat
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

import logging
import mock
import os

from nodepool import config as nodepool_config
from nodepool import tests
from nodepool import zk
from nodepool.cmd.config_validator import ConfigValidator


class TestDriverStatic(tests.DBTestCase):
    log = logging.getLogger("nodepool.TestDriverStatic")

    def test_static_validator(self):
        config = os.path.join(os.path.dirname(tests.__file__),
                              'fixtures', 'config_validate',
                              'static_error.yaml')
        validator = ConfigValidator(config)
        ret = validator.validate()
        self.assertEqual(ret, 1)

    def test_static_config(self):
        configfile = self.setup_config('static.yaml')
        config = nodepool_config.loadConfig(configfile)
        self.assertIn('static-provider', config.providers)

    def test_static_basic(self):
        '''
        Test that basic node registration works.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].provider, "static-provider")
        self.assertEqual(nodes[0].pool, "main")
        self.assertEqual(nodes[0].launcher, "static driver")
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].hostname, 'fake-host-1')
        self.assertEqual(nodes[0].interface_ip, 'fake-host-1')
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[0].connection_port, 22022)
        self.assertEqual(nodes[0].connection_type, 'ssh')
        self.assertEqual(nodes[0].host_keys, ['ssh-rsa FAKEKEY'])
        self.assertEqual(nodes[0].attributes,
                         {'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(nodes[0].python_path, 'auto')
        self.assertIsNone(nodes[0].shell_type)

    def test_static_python_path(self):
        '''
        Test that static python-path works.
        '''
        configfile = self.setup_config('static-python-path.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].python_path, "/usr/bin/python3")

        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].python_path, "/usr/bin/python3")

    def test_static_multiname(self):
        '''
        Test that multi name node (re-)registration works.
        '''
        configfile = self.setup_config('static-multiname.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label', 1)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].username, 'zuul')

        nodes = self.waitForNodes('other-label', 1)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].username, 'zuul-2')

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        registered_labels = {n.type[0] for n in self.zk.nodeIterator()}
        self.assertEqual(registered_labels, {'fake-label', 'other-label'})

    def test_static_unresolvable(self):
        '''
        Test that basic node registration works.
        '''
        configfile = self.setup_config('static-unresolvable.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].provider, "static-provider")
        self.assertEqual(nodes[0].pool, "main")
        self.assertEqual(nodes[0].launcher, "static driver")
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].hostname, 'fake-host-1')
        self.assertEqual(nodes[0].interface_ip, 'fake-host-1')
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[0].connection_port, 22022)
        self.assertEqual(nodes[0].connection_type, 'ssh')
        self.assertEqual(nodes[0].host_keys, ['ssh-rsa FAKEKEY'])

    def test_static_node_increase(self):
        '''
        Test that adding new nodes to the config creates additional nodes.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.log.debug("Waiting for additional node")
        self.replace_config(configfile, 'static-2-nodes.yaml')
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)

    def test_static_node_decrease(self):
        '''
        Test that removing nodes from the config removes nodes.
        '''
        configfile = self.setup_config('static-2-nodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)

        self.log.debug("Waiting for node decrease")
        self.replace_config(configfile, 'static-basic.yaml')
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].hostname, 'fake-host-1')

    def test_static_parallel_increase(self):
        '''
        Test that increasing max-parallel-jobs creates additional nodes.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.log.debug("Waiting for additional node")
        self.replace_config(configfile, 'static-parallel-increase.yaml')
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)

    def test_static_parallel_decrease(self):
        '''
        Test that decreasing max-parallel-jobs deletes nodes.
        '''
        configfile = self.setup_config('static-parallel-increase.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)

        self.log.debug("Waiting for node decrease")
        self.replace_config(configfile, 'static-basic.yaml')
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

    def test_static_node_update(self):
        '''
        Test that updates a static node on config change.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.log.debug("Waiting for new label")
        self.replace_config(configfile, 'static-update.yaml')
        nodes = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes), 1)
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)
        self.assertEqual(nodes[0].username, 'admin')
        self.assertEqual(nodes[0].connection_port, 5986)
        self.assertEqual(nodes[0].connection_type, 'winrm')
        self.assertEqual(nodes[0].host_keys, [])

    def test_static_node_update_startup(self):
        '''
        Test that updates a static node on config change at startup.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')

        pool.stop()
        configfile = self.setup_config('static-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for new label")
        nodes = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes), 1)
        # Check that the node was updated and not re-created
        self.assertEqual(nodes[0].id, "0000000000")
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)

    def test_static_multilabel(self):
        configfile = self.setup_config('static-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        nodes = self.waitForNodes('fake-label')
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)

    def test_static_handler(self):
        configfile = self.setup_config('static.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        node = self.waitForNodes('fake-label')
        self.waitForNodes('fake-concurrent-label', 2)

        node = node[0]
        self.log.debug("Marking first node as used %s", node.id)
        node.state = zk.USED
        self.zk.storeNode(node)
        self.waitForNodeDeletion(node)

        self.log.debug("Waiting for node to be re-available")
        node = self.waitForNodes('fake-label')
        self.assertEqual(len(node), 1)

    def test_static_waiting_handler(self):
        configfile = self.setup_config('static-2-nodes-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        req_waiting = zk.NodeRequest()
        req_waiting.state = zk.REQUESTED
        req_waiting.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting)
        req_waiting = self.waitForNodeRequest(req_waiting, zk.PENDING)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label2')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        req_waiting = self.zk.getNodeRequest(req_waiting.id)
        self.assertEqual(req_waiting.state, zk.PENDING)

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)
        self.waitForNodeRequest(req_waiting, zk.FULFILLED)

    def test_static_ignore_assigned_ready_nodes(self):
        """Regression test to not touch assigned READY nodes"""
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        # Make sure the cleanup worker is called that reallocated the node
        pool.cleanup_interval = .1
        pool.start()

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        req_waiting = zk.NodeRequest()
        req_waiting.state = zk.REQUESTED
        req_waiting.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting)
        req_waiting = self.waitForNodeRequest(req_waiting, zk.PENDING)

        # Make sure the node is not reallocated
        node = self.zk.getNode(req.nodes[0])
        self.assertIsNotNone(node)

    def test_static_waiting_handler_order(self):
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        req_waiting1 = zk.NodeRequest()
        req_waiting1.state = zk.REQUESTED
        req_waiting1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting1)
        req_waiting1 = self.waitForNodeRequest(req_waiting1, zk.PENDING)

        req_waiting2 = zk.NodeRequest()
        req_waiting2.state = zk.REQUESTED
        req_waiting2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting2)
        req_waiting2 = self.waitForNodeRequest(req_waiting2, zk.PENDING)

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)

        req_waiting1 = self.waitForNodeRequest(req_waiting1, zk.FULFILLED)
        req_waiting2 = self.zk.getNodeRequest(req_waiting2.id)
        self.assertEqual(req_waiting2.state, zk.PENDING)

        node_waiting1 = self.zk.getNode(req_waiting1.nodes[0])
        self.zk.lockNode(node_waiting1)
        node_waiting1.state = zk.USED
        self.zk.storeNode(node_waiting1)
        self.zk.unlockNode(node_waiting1)

        self.waitForNodeRequest(req_waiting2, zk.FULFILLED)

    def test_static_handler_race_cleanup(self):
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        node = self.waitForNodes('fake-label')[0]

        # Create the result of a race between re-registration of a
        # ready node and a new building node.
        data = node.toDict()
        data.update({
            "state": zk.BUILDING,
            "hostname": "",
            "username": "",
            "connection_port": 22,
        })
        building_node = zk.Node.fromDict(data)
        self.zk.storeNode(building_node)
        self.zk.lockNode(building_node)

        # Node will be deregistered and assigned to the building node
        self.waitForNodeDeletion(node)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(building_node.id, nodes[0].id)

        building_node.state = zk.USED
        self.zk.storeNode(building_node)
        self.zk.unlockNode(building_node)
        self.waitForNodeDeletion(building_node)

    def test_static_multinode_handler(self):
        configfile = self.setup_config('static.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.node_types.append('fake-concurrent-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 2)

    def test_static_multiprovider_handler(self):
        configfile = self.setup_config('multiproviders.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.wait_for_config(pool)
        manager = pool.getProviderManager('openstack-provider')
        manager._client.create_image(name="fake-image")

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-static-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-openstack-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)

    def test_static_request_handled(self):
        '''
        Test that a node is reregistered after handling a request.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)
        self.assertEqual(req.nodes[0], nodes[0].id)

        # Mark node as used
        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        # Our single node should have been used, deleted, then reregistered
        new_nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(nodes[0].hostname, new_nodes[0].hostname)

    def test_liveness_check(self):
        '''
        Test liveness check during request handling.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')

        with mock.patch("nodepool.nodeutils.nodescan") as nodescan_mock:
            nodescan_mock.side_effect = OSError
            self.zk.storeNodeRequest(req)
            self.waitForNodeDeletion(nodes[0])

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)

        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)
        self.assertNotEqual(req.nodes[0], nodes[0].id)

    def test_host_key_checking_toggle(self):
        """Test that host key checking can be disabled"""
        configfile = self.setup_config('static-no-check.yaml')
        with mock.patch("nodepool.nodeutils.nodescan") as nodescan_mock:
            pool = self.useNodepool(configfile, watermark_sleep=1)
            pool.start()
            nodes = self.waitForNodes('fake-label')
            self.assertEqual(len(nodes), 1)
            nodescan_mock.assert_not_called()

    def test_static_shell_type(self):
        '''
        Test that static python-path works.
        '''
        configfile = self.setup_config('static-shell-type.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].shell_type, "cmd")

        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].shell_type, "cmd")

    def test_missing_static_node(self):
        """Test that a missing static node is added"""
        configfile = self.setup_config('static-2-nodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.start()

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)

        self.zk.deleteNode(nodes[0])

        self.log.debug("Waiting for node to transition to ready again")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
