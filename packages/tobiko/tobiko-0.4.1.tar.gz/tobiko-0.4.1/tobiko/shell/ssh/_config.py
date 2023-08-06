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

import collections
import os
import typing  # noqa
import urllib

from oslo_log import log
import paramiko

import tobiko


LOG = log.getLogger(__name__)


def ssh_config(config_files=None):
    if config_files:
        fixture = SSHConfigFixture(config_files=config_files)
    else:
        fixture = SSHConfigFixture
    return tobiko.setup_fixture(fixture)


def ssh_host_config(host=None, config_files=None):
    return ssh_config(config_files=config_files).lookup(host)


class SSHDefaultConfigFixture(tobiko.SharedFixture):

    conf = None

    def setup_fixture(self):
        self.conf = tobiko.tobiko_config().ssh

    def __getattr__(self, name):
        return getattr(self.conf, name)


class SSHConfigFixture(tobiko.SharedFixture):

    default = tobiko.required_setup_fixture(SSHDefaultConfigFixture)

    config_files = None
    config = None

    def __init__(self, config_files=None):
        super(SSHConfigFixture, self).__init__()
        if config_files:
            self.config_files = tuple(config_files)
        else:
            self.config_files = self.default.config_files

    def setup_fixture(self):
        self.setup_ssh_config()

    def setup_ssh_config(self):
        self.config = paramiko.SSHConfig()
        for config_file in self.config_files:
            config_file = tobiko.tobiko_config_path(config_file)
            if os.path.exists(config_file):
                LOG.debug("Parsing %r config file...", config_file)
                with open(config_file) as f:
                    self.config.parse(f)
                LOG.debug("File %r parsed.", config_file)

    def lookup(self,
               host: typing.Optional[str] = None,
               hostname: typing.Optional[str] = None,
               username: typing.Optional[str] = None,
               port: typing.Optional[int] = None):
        if host and ('@' in host or ':' in host):
            host_url = urllib.parse.urlparse(f"ssh://{host}")
            hostname = hostname or host_url.hostname or None
            username = username or host_url.username or None
            port = port or host_url.port or None
        else:
            hostname = hostname or host

        if hostname and self.config:
            host_config: dict = self.config.lookup(hostname)
        else:
            host_config = {}

        # remove unsupported directive
        include_files = host_config.pop('include', None)
        if include_files:
            LOG.warning('Ignoring unsupported directive: Include %s',
                        include_files)
        if hostname:
            host_config.setdefault('hostname', hostname)
        if username:
            host_config.setdefault('user', username)
        if port:
            host_config.setdefault('port', port)
        return SSHHostConfig(host=host,
                             ssh_config=self,
                             host_config=host_config,
                             config_files=self.config_files)

    def __repr__(self):
        return "{class_name!s}(config_files={config_files!r})".format(
            class_name=type(self).__name__, config_files=self.config_files)


class SSHHostConfig(collections.namedtuple('SSHHostConfig', ['host',
                                                             'ssh_config',
                                                             'host_config',
                                                             'config_files'])):

    default = tobiko.required_setup_fixture(SSHDefaultConfigFixture)

    @property
    def hostname(self):
        return self.host_config.get('hostname', self.host)

    @property
    def port(self):
        return (self.host_config.get('port') or
                self.default.port)

    @property
    def username(self):
        return (self.host_config.get('user') or
                self.default.username)

    @property
    def key_filename(self):
        key_filename = []
        host_config_key_files = self.host_config.get('identityfile')
        if host_config_key_files:
            for filename in host_config_key_files:
                if filename:
                    key_filename.append(tobiko.tobiko_config_path(filename))

        default_key_files = self.default.key_file
        if default_key_files:
            for filename in default_key_files:
                if filename:
                    key_filename.append(tobiko.tobiko_config_path(filename))

        return key_filename

    @property
    def proxy_jump(self):
        proxy_jump = (self.host_config.get('proxyjump') or
                      self.default.proxy_jump)
        if not proxy_jump:
            return None

        proxy_hostname = self.ssh_config.lookup(proxy_jump).hostname
        if ({proxy_jump, proxy_hostname} & {self.host, self.hostname}):
            # Avoid recursive proxy jump definition
            return None

        return proxy_jump

    @property
    def proxy_command(self):
        return (self.host_config.get('proxycommand') or
                self.default.proxy_command)

    @property
    def allow_agent(self):
        return (is_yes(self.host_config.get('forwardagent')) or
                self.default.allow_agent)

    @property
    def compress(self):
        return (is_yes(self.host_config.get('compression')) or
                self.default.compress)

    @property
    def timeout(self):
        return (self.host_config.get('connetcttimeout') or
                self.default.timeout)

    @property
    def connection_attempts(self):
        return (self.host_config.get('connectionattempts') or
                self.default.connection_attempts)

    @property
    def connection_interval(self):
        return self.default.connection_interval

    @property
    def connection_timeout(self):
        return self.default.connection_timeout

    @property
    def connect_parameters(self):
        return dict(hostname=self.hostname,
                    port=self.port,
                    username=self.username,
                    key_filename=self.key_filename,
                    compress=self.compress,
                    timeout=self.timeout,
                    allow_agent=self.allow_agent,
                    connection_attempts=self.connection_attempts,
                    connection_interval=self.connection_interval,
                    connection_timeout=self.connection_timeout)


def is_yes(value):
    return value and str(value).lower() == 'yes'
