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

from tobiko.openstack import keystone
from tobiko.openstack import nova
from tobiko.tests.unit import openstack
from tobiko.tests.unit.openstack import test_client


class NovaClientFixtureTest(test_client.OpenstackClientFixtureTest):

    def create_client(self, session=None):
        return nova.NovaClientFixture(session=session)


class GetNovaClientTest(openstack.OpenstackTest):

    def test_get_nova_client(self, session=None, shared=True):
        client1 = nova.get_nova_client(session=session, shared=shared)
        client2 = nova.get_nova_client(session=session, shared=shared)
        if shared:
            self.assertIs(client1, client2)
        else:
            self.assertIsNot(client1, client2)
        self.assertIsInstance(client1, nova.CLIENT_CLASSES)
        self.assertIsInstance(client2, nova.CLIENT_CLASSES)

    def test_get_nova_client_with_not_shared(self):
        self.test_get_nova_client(shared=False)

    def test_get_nova_client_with_session(self):
        session = keystone.get_keystone_session()
        self.test_get_nova_client(session=session)


class NeutronClientTest(openstack.OpenstackTest):

    def test_neutron_client_with_none(self):
        default_client = nova.get_nova_client()
        client = nova.nova_client(None)
        self.assertIsInstance(client, nova.CLIENT_CLASSES)
        self.assertIs(default_client, client)

    def test_neutron_client_with_client(self):
        default_client = nova.get_nova_client()
        client = nova.nova_client(default_client)
        self.assertIsInstance(client, nova.CLIENT_CLASSES)
        self.assertIs(default_client, client)

    def test_neutron_client_with_fixture(self):
        fixture = nova.NovaClientFixture()
        client = nova.nova_client(fixture)
        self.assertIsInstance(client, nova.CLIENT_CLASSES)
        self.assertIs(client, fixture.client)
