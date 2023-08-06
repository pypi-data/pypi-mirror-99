# Copyright 2017 Red Hat
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
#
# See the License for the specific language governing permissions and
# limitations under the License.

import voluptuous as v

from nodepool.driver import ConfigPool
from nodepool.driver import ProviderConfig
from nodepool.config import as_list


class StaticPool(ConfigPool):
    def __init__(self):
        self.name = None
        self.nodes = []
        # The StaticProviderConfig that owns this pool.
        self.provider = None

        # Initialize base class attributes
        super().__init__()

    def __eq__(self, other):
        if isinstance(other, StaticPool):
            return (super().__eq__(other) and
                    other.name == self.name and
                    other.nodes == self.nodes)
        return False

    def __repr__(self):
        return "<StaticPool %s>" % self.name

    def load(self, pool_config, full_config):
        super().load(pool_config)
        self.name = pool_config['name']
        # WARNING: This intentionally changes the type!
        self.labels = set()
        for node in pool_config.get('nodes', []):
            self.nodes.append({
                'name': node['name'],
                'labels': as_list(node['labels']),
                'host-key': as_list(node.get('host-key', [])),
                'host-key-checking': bool(node.get('host-key-checking', True)),
                'timeout': int(node.get('timeout', 5)),
                # Read ssh-port values for backward compat, but prefer port
                'connection-port': int(
                    node.get('connection-port', node.get('ssh-port', 22))),
                'connection-type': node.get('connection-type', 'ssh'),
                'shell-type': node.get('shell-type', None),
                'username': node.get('username', 'zuul'),
                'max-parallel-jobs': int(node.get('max-parallel-jobs', 1)),
                'python-path': node.get('python-path', 'auto'),
            })
            if isinstance(node['labels'], str):
                for label in node['labels'].split():
                    self.labels.add(label)
                    full_config.labels[label].pools.append(self)
            elif isinstance(node['labels'], list):
                for label in node['labels']:
                    self.labels.add(label)
                    full_config.labels[label].pools.append(self)


class StaticProviderConfig(ProviderConfig):
    def __init__(self, *args, **kwargs):
        self.__pools = {}
        super().__init__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, StaticProviderConfig):
            return (super().__eq__(other) and
                    other.manage_images == self.manage_images and
                    other.pools == self.pools)
        return False

    @property
    def pools(self):
        return self.__pools

    @property
    def manage_images(self):
        return False

    def load(self, config):
        for pool in self.provider.get('pools', []):
            pp = StaticPool()
            pp.load(pool, config)
            pp.provider = self
            self.pools[pp.name] = pp

    def getSchema(self):
        pool_node = {
            v.Required('name'): str,
            v.Required('labels'): v.Any(str, [str]),
            'username': str,
            'timeout': int,
            'host-key-checking': bool,
            'host-key': v.Any(str, [str]),
            'connection-port': int,
            'connection-type': str,
            'shell-type': str,
            'max-parallel-jobs': int,
            'python-path': str,
        }
        pool = ConfigPool.getCommonSchemaDict()
        pool.update({
            'name': str,
            'nodes': [pool_node],
        })
        schema = ProviderConfig.getCommonSchemaDict()
        schema.update({'pools': [pool]})
        return v.Schema(schema)

    def getSupportedLabels(self, pool_name=None):
        labels = set()
        for pool in self.pools.values():
            if not pool_name or (pool.name == pool_name):
                labels.update(pool.labels)
        return labels
