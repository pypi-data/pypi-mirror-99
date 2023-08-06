# Copyright 2019 Red Hat
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from __future__ import absolute_import

import collections

import tobiko
from tobiko.openstack import keystone
from tobiko.openstack.neutron import _client


@keystone.skip_unless_has_keystone_credentials()
class NetworkingExtensionsFixture(tobiko.SharedFixture):

    client = None
    extensions = None

    def setup_fixture(self):
        self.setup_client()
        self.get_networking_extensions()

    def setup_client(self):
        self.client = _client.get_neutron_client()

    def get_networking_extensions(self):
        extensions = self.client.list_extensions()
        if isinstance(extensions, collections.Mapping):
            extensions = extensions['extensions']
        self.extensions = frozenset(e['alias'] for e in extensions)


def get_networking_extensions():
    return tobiko.setup_fixture(NetworkingExtensionsFixture).extensions


def missing_networking_extensions(*extensions):
    return sorted(frozenset(extensions) - get_networking_extensions())


def has_networking_extensions(*extensions):
    return not missing_networking_extensions(*extensions)


def skip_if_missing_networking_extensions(*extensions):
    return tobiko.skip_if('missing networking extensions: {return_value!r}',
                          missing_networking_extensions, *extensions)


if __name__ == '__main__':
    import sys
    sys.stdout.write('\n'.join(sorted(get_networking_extensions())))
    sys.stdout.flush()
