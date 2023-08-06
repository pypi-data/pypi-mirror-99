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

import io
import typing  # noqa

from oslo_log import log

import tobiko
from tobiko.shell.sh import _command
from tobiko.shell.sh import _exception
from tobiko.shell.sh import _io


LOG = log.getLogger(__name__)


def process(command=None, environment=None, timeout: tobiko.Seconds = None,
            shell=None, stdin=None, stdout=None, stderr=None, ssh_client=None,
            sudo=None, **kwargs):
    kwargs.update(command=command, environment=environment, timeout=timeout,
                  shell=shell, stdin=stdin, stdout=stdout, stderr=stderr,
                  sudo=sudo)
    if timeout is not None:
        if timeout < 0.:
            raise ValueError("Invalid timeout for executing process: "
                             "{!r}".format(timeout))
    try:
        from tobiko.shell.sh import _ssh
        from tobiko.shell import ssh
    except ImportError:
        if ssh_client:
            raise
    else:
        if ssh_client is None:
            ssh_client = ssh.ssh_proxy_client()
        if ssh_client:
            return _ssh.ssh_process(ssh_client=ssh_client, **kwargs)

    from tobiko.shell.sh import _local
    return _local.local_process(**kwargs)


class Parameters(object):

    def __init__(self, **kwargs):
        cls = type(self)
        for name, value in kwargs.items():
            if value is not None:
                if not hasattr(cls, name):
                    raise ValueError('Invalid parameter: {!s}'.format(name))
                setattr(self, name, value)


class ShellProcessParameters(Parameters):

    command = None
    environment = None
    current_dir = None
    timeout: tobiko.Seconds = None
    shell = None
    stdin = False
    stdout = True
    stderr = True
    buffer_size = io.DEFAULT_BUFFER_SIZE
    poll_interval = 1.
    sudo = None
    network_namespace = None
    retry_count: typing.Optional[int] = 3
    retry_interval: tobiko.Seconds = 5.
    retry_timeout: tobiko.Seconds = 120.


class ShellProcessFixture(tobiko.SharedFixture):

    command = None
    process: typing.Any = None
    stdin = None
    stdout = None
    stderr = None

    _exit_status = None

    def __init__(self, **kwargs):
        super(ShellProcessFixture, self).__init__()
        self.parameters = self.init_parameters(**kwargs)

    def init_parameters(self, **kwargs) -> ShellProcessParameters:
        return ShellProcessParameters(**kwargs)

    def execute(self):
        return tobiko.setup_fixture(self)

    def setup_fixture(self):
        parameters = self.parameters

        self.setup_command()
        self.setup_process()

        if parameters.stdin:
            self.setup_stdin()
        if parameters.stdout:
            self.setup_stdout()
        if parameters.stderr:
            self.setup_stderr()

    def setup_command(self):
        command = _command.shell_command(self.parameters.command)
        network_namespace = self.parameters.network_namespace
        sudo = self.parameters.sudo

        shell = self.parameters.shell
        if shell:
            if shell is True:
                shell = default_shell_command()
            else:
                shell = _command.shell_command(shell)
            command = shell + [str(command)]
        else:
            command = _command.shell_command(command)

        if network_namespace:
            if sudo is None:
                sudo = True
            command = network_namespace_command(network_namespace, command)

        if sudo:
            if sudo is True:
                sudo = default_sudo_command()
            else:
                sudo = _command.shell_command(sudo)
            command = sudo + command

        self.command = command

    def setup_process(self):
        if self._exit_status:
            del self._exit_status
        self.process = self.create_process()
        self.addCleanup(self.close)

    def setup_stdin(self):
        raise NotImplementedError

    def setup_stdout(self):
        raise NotImplementedError

    def setup_stderr(self):
        raise NotImplementedError

    def create_process(self):
        raise NotImplementedError

    def close_stdin(self):
        stdin = self.stdin
        if stdin is not None:
            try:
                stdin.closed or stdin.close()
            except Exception:
                LOG.exception("Error closing STDIN stream: %r", self.stdin)

    def close_stdout(self):
        stdout = self.stdout
        if stdout is not None:
            try:
                stdout.closed or stdout.close()
            except Exception:
                LOG.exception("Error closing STDOUT stream: %r", self.stdout)

    def close_stderr(self):
        stderr = self.stderr
        if stderr is not None:
            try:
                stderr.closed or stderr.close()
            except Exception:
                LOG.exception("Error closing STDERR stream: %r", self.stderr)

    def close(self, timeout: tobiko.Seconds = None):
        self.close_stdin()
        try:
            # Drain all incoming data from STDOUT and STDERR
            self.wait(timeout=timeout)
        finally:
            self._terminate()

    def _terminate(self):
        self.close_stdout()
        self.close_stderr()
        exit_status = None
        try:
            exit_status = self.get_exit_status()
        finally:
            if exit_status is None:
                try:
                    self.kill()
                except Exception:
                    LOG.exception('Error killing process: %r', self.command)

    def __getattr__(self, name):
        try:
            # Get attributes from parameters class
            return getattr(self.parameters, name)
        except AttributeError as ex:
            message = "object {!r} has not attribute {!r}".format(self, name)
            raise AttributeError(message) from ex

    def kill(self):
        raise NotImplementedError

    def poll_exit_status(self):
        raise NotImplementedError

    def get_exit_status(self, timeout: tobiko.Seconds = None):
        if timeout is None:
            timeout = self.parameters.timeout
        exit_status = self._get_exit_status(timeout=timeout)
        if exit_status is not None:
            return exit_status

        ex = _exception.ShellTimeoutExpired(
            command=str(self.command),
            timeout=timeout,
            stdin=str_from_stream(self.stdin),
            stdout=str_from_stream(self.stdout),
            stderr=str_from_stream(self.stderr))
        LOG.debug("Timed out while waiting for command termination:\n%s",
                  self.command)
        raise ex

    def _get_exit_status(self, timeout):
        raise NotImplementedError

    @property
    def exit_status(self):
        exit_status = self._exit_status
        if exit_status is None:
            exit_status = self.poll_exit_status()
            if exit_status is not None:
                self._exit_status = exit_status
        return exit_status

    @property
    def is_running(self):
        return self.exit_status is None

    def check_is_running(self):
        exit_status = self.exit_status
        if exit_status is not None:
            raise _exception.ShellProcessTerminated(
                command=str(self.command),
                exit_status=int(exit_status),
                stdin=str_from_stream(self.stdin),
                stdout=str_from_stream(self.stdout),
                stderr=str_from_stream(self.stderr))

    def check_stdin_is_opened(self):
        if self.stdin.closed:
            raise _exception.ShellStdinClosed(
                command=str(self.command),
                stdin=str_from_stream(self.stdin),
                stdout=str_from_stream(self.stdout),
                stderr=str_from_stream(self.stderr))

    def send_all(self, data, **kwargs):
        self.communicate(stdin=data, **kwargs)
        self.stdin.flush()

    def receive_all(self, **kwargs):
        self.communicate(receive_all=True, **kwargs)

    def wait(self, timeout: tobiko.Seconds = None, receive_all=True,
             **kwargs):
        self.communicate(timeout=timeout, receive_all=receive_all,
                         **kwargs)

    def communicate(self, stdin=None, stdout=True, stderr=True,
                    timeout: tobiko.Seconds = None,
                    receive_all=False, buffer_size=None):
        timeout = tobiko.to_seconds(timeout)

        # Avoid waiting for data in the first loop
        poll_interval = 0.
        streams = _io.select_opened_files([stdin and self.stdin,
                                           stdout and self.stdout,
                                           stderr and self.stderr])
        for attempt in tobiko.retry(timeout=timeout):
            if not self._is_communicating(streams=streams, send=stdin,
                                          receive=receive_all):
                break

            # Remove closed streams
            streams = _io.select_opened_files(streams)

            # Select ready streams
            read_ready, write_ready = _io.select_files(
                files=streams, timeout=poll_interval)
            if read_ready or write_ready:
                # Avoid waiting for data the next time
                poll_interval = 0.
                if self.stdin in write_ready:
                    # Write data to remote STDIN
                    stdin = self._write_to_stdin(stdin)
                    if not stdin:
                        streams.remove(self.stdin)
                if self.stdout in read_ready:
                    # Read data from remote STDOUT
                    stdout = self._read_from_stdout(buffer_size=buffer_size)
                    if not stdout:
                        streams.remove(self.stdout)
                if self.stderr in read_ready:
                    # Read data from remote STDERR
                    stderr = self._read_from_stderr(buffer_size=buffer_size)
                    if not stderr:
                        streams.remove(self.stderr)
            else:
                self._check_communicate_timeout(attempt=attempt,
                                                timeout=timeout)
                # Wait for data in the following loops
                poll_interval = self.parameters.poll_interval
                LOG.debug(f"Waiting for process data {poll_interval} "
                          f"seconds... \n"
                          f"  command: '{self.command}'\n"
                          f"  attempt: {attempt.details}\n"
                          f"  streams: {streams}")

    def _check_communicate_timeout(self, attempt: tobiko.RetryAttempt,
                                   timeout: tobiko.Seconds):
        try:
            attempt.check_limits()
        except tobiko.RetryTimeLimitError:
            pass
        else:
            return
        # Eventually raises ShellCommandTimeout exception
        self.get_exit_status(timeout=timeout)
        raise StopIteration

    def _is_communicating(self, streams, send, receive):
        if send and self.stdin in streams:
            return True
        elif receive and {self.stdout, self.stderr} & streams:
            return True
        else:
            return False

    def _write_to_stdin(self, data, check=True):
        """Write data to STDIN"""
        if check:
            self.check_stdin_is_opened()
        sent_bytes = self.stdin.write(data)
        if sent_bytes:
            return data[sent_bytes:] or None
        else:
            LOG.debug("%r closed by peer on %r", self.stdin, self)
            self.stdin.close()
            return data

    def _read_from_stdout(self, buffer_size=None):
        """Read data from remote stream"""
        # Read data from remote stream
        chunk = self.stdout.read(buffer_size)
        if chunk:
            return chunk
        else:
            LOG.debug("%r closed by peer on %r", self.stdout, self)
            self.stdout.close()
            return None

    def _read_from_stderr(self, buffer_size=None):
        """Read data from remote stream"""
        # Read data from remote stream
        chunk = self.stderr.read(buffer_size)
        if chunk:
            return chunk
        else:
            LOG.debug("%r closed by peer on %r", self.stderr, self)
            self.stderr.close()
            return None

    def check_exit_status(self, expected_status=0):
        exit_status = self.poll_exit_status()
        if exit_status is None:
            time_left = self.check_timeout()
            ex = _exception.ShellProcessNotTerminated(
                command=str(self.command),
                time_left=time_left,
                stdin=self.stdin,
                stdout=self.stdout,
                stderr=self.stderr)
            raise ex

        exit_status = int(exit_status)
        if expected_status != exit_status:
            ex = _exception.ShellCommandFailed(
                command=str(self.command),
                exit_status=exit_status,
                stdin=str_from_stream(self.stdin),
                stdout=str_from_stream(self.stdout),
                stderr=str_from_stream(self.stderr))
            raise ex


def merge_dictionaries(*dictionaries):
    merged = {}
    for d in dictionaries:
        if d:
            merged.update(d)
    return merged


def str_from_stream(stream):
    if stream is not None:
        return str(stream)
    else:
        return None


def default_shell_command():
    from tobiko import config
    CONF = config.CONF
    return _command.shell_command(CONF.tobiko.shell.sudo.command)


def default_sudo_command():
    from tobiko import config
    CONF = config.CONF
    return _command.shell_command(CONF.tobiko.shell.sudo)


def network_namespace_command(network_namespace, command):
    return _command.shell_command(['/sbin/ip', 'netns', 'exec',
                                   network_namespace]) + command
