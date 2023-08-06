# Copyright (c) 2019 Red Hat
# All Rights Reserved.
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

import testtools

import tobiko
from tobiko.shell import ip
from tobiko.shell import ping
from tobiko.shell import sh
from tobiko.openstack import topology


class OpenstackNodesTest(testtools.TestCase):

    topology = tobiko.required_setup_fixture(
        topology.get_default_openstack_topology_class())

    def test_public_ips(self):
        ips = dict()
        for node in self.topology.nodes:
            ping.ping(node.public_ip).assert_replied()
            other = ips.setdefault(node.public_ip, node)
            if node is not other:
                tobiko.fail("Nodes {!r} and {!r} have the same IP: {!s}",
                            node.name, other.name, node.public_ip)

    def test_hostnames(self):
        hostnames = dict()
        for node in self.topology.nodes:
            hostname = sh.get_hostname(ssh_client=node.ssh_client)
            self.assertTrue(hostname.startswith(node.name))
            other = hostnames.setdefault(hostname, node)
            if node is not other:
                tobiko.fail("Nodes {!r} and {!r} have the same hostname: {!r}",
                            node.name, other.name, hostname)

    def test_network_namespaces(self):
        for node in self.topology.nodes:
            namespaces_ips = {}
            namespaces = ip.list_network_namespaces(ssh_client=node.ssh_client)
            for namespace in namespaces:
                ips = ip.list_ip_addresses(ssh_client=node.ssh_client,
                                           network_namespace=namespace)
                other_ips = namespaces_ips.setdefault(namespace, ips)
                if ips is not other_ips:
                    tobiko.fail("Duplicate network namespace {!r} in node "
                                "{!r}: {!r}, {!r}", namespace, node.name,
                                other_ips, ips)
