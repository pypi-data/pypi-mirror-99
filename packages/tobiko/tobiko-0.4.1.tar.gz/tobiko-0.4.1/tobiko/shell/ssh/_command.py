# Copyright (c) 2019 Red Hat, Inc.
#
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

import subprocess

import six

from tobiko.shell.ssh import _config


def ssh_login(hostname, username=None, port=None):
    login = hostname
    if port:
        login += ':' + str(port)
    if username:
        login = username + '@' + login
    return login


def ssh_command(host, username=None, port=None, command=None,
                config_files=None, host_config=None, proxy_command=None,
                key_filename=None, **options):
    host_config = host_config or _config.ssh_host_config(
        host=host, config_files=config_files)

    command = command or host_config.default.command.split()
    if isinstance(command, six.string_types):
        command = command.split()

    hostname = host_config.hostname
    username = username or host_config.username
    command += [ssh_login(hostname=hostname, username=username)]

    #     if host_config.default.debug:
    #         command += ['-vvvvvv']

    port = port or host_config.port
    if port:
        command += ['-p', str(port)]

    if key_filename:
        command += ['-i', key_filename]

    if proxy_command:
        if not isinstance(proxy_command, six.string_types):
            proxy_command = subprocess.list2cmdline([str(a)
                                                     for a in proxy_command])
        options['ProxyCommand'] = proxy_command

    for name, value in host_config.host_config.items():
        if name not in {'hostname', 'port', 'user'}:
            options.setdefault(name, value)
    options.setdefault('UserKnownHostsFile', '/dev/null')
    options.setdefault('StrictHostKeyChecking', 'no')
    options.setdefault('LogLevel', 'quiet')
    options.setdefault('ConnectTimeout', int(host_config.timeout))
    options.setdefault('ConnectionAttempts', host_config.connection_attempts)
    if options:
        for name, value in sorted(options.items()):
            name = name.replace('_', '')
            command += ['-o', '{!s}={!s}'.format(name, value)]

    return command
