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

import itertools

from oslo_config import cfg

GROUP_NAME = 'neutron'
OPTIONS = [
    cfg.StrOpt('external_network',
               help="Network for creating ports on an external network"),
    cfg.StrOpt('floating_network',
               help="Network for creating floating IPs"),
    cfg.StrOpt('ipv4_cidr',
               default='10.100.0.0/16',
               help="The CIDR block to allocate IPv4 subnets from"),
    cfg.IntOpt('ipv4_prefixlen',
               default=24,
               help="The mask bits for IPv4 subnets"),
    cfg.ListOpt('ipv4_dns_nameservers',
                default=None,
                help="List of nameservers IPv4 addresses"),
    cfg.StrOpt('ipv6_cidr',
               default='2001:db8::/48',
               help="The CIDR block to allocate IPv6 subnets from"),
    cfg.IntOpt('ipv6_prefixlen',
               default=64,
               help="The mask bits for IPv6 subnets"),
    cfg.ListOpt('ipv6_dns_nameservers',
                default=None,
                help="List of nameservers IPv6 addresses"),
    cfg.IntOpt('custom_mtu_size',
               default=1350,
               help=("Customized maximum transfer unit size\n"
                     "Notes:\n"
                     " - MTU values as small as 1000 has been seen "
                     "breaking networking binding due to an "
                     "unknown cause.\n"
                     " - Too big MTU values (like greater than 1400)"
                     " may be refused during network creation")),
    cfg.StrOpt('nameservers_host',
               default=None,
               help="Host where nameservers files are located"),
    cfg.ListOpt('nameservers_filenames',
                default=['/etc/resolv.conf'],
                help="File to parse for getting default nameservers list")
]


def register_tobiko_options(conf):
    conf.register_opts(group=cfg.OptGroup(GROUP_NAME), opts=OPTIONS)


def list_options():
    return [(GROUP_NAME, itertools.chain(OPTIONS))]
