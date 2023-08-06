# Copyright (c) 2020 Red Hat, Inc.
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
import re
import time

import tobiko
from tobiko.shell.sh import _execute
from tobiko.shell.sh import _hostname


class PsError(tobiko.TobikoException):
    message = "Unable to list processes from host: {error}"


class PsWaitTimeout(PsError):
    message = ("Process(es) still running on host {hostname!r} after "
               "{timeout} seconds:\n{processes!s}")


IS_KERNEL_RE = re.compile('^\\[.*\\]$')


class PsProcess(collections.namedtuple('PsProcess', ['ssh_client',
                                                     'pid',
                                                     'command'])):
    """Process listed by ps command
    """

    @property
    def is_kernel(self):
        return IS_KERNEL_RE.match(self.command) is not None


def list_kernel_processes(**list_params):
    return list_processes(is_kernel=True, **list_params)


def list_all_processes(**list_params):
    return list_processes(is_kernel=None, **list_params)


def list_processes(pid=None, command=None, is_kernel=False, ssh_client=None,
                   **execute_params):
    """Returns the number of seconds passed since last host reboot

    It reads and parses remote special file /proc/uptime and returns a floating
    point value that represents the number of seconds passed since last host
    reboot
    """
    result = _execute.execute('ps -A', expect_exit_status=None,
                              ssh_client=ssh_client, **execute_params)
    output = result.stdout and result.stdout.strip()
    if result.exit_status or not output:
        raise PsError(error=result.stderr)

    # Extract a list of PsProcess instances from table body
    processes = tobiko.Selection()
    for process_data in parse_table(lines=output.splitlines(),
                                    schema=PS_TABLE_SCHEMA):
        processes.append(PsProcess(ssh_client=ssh_client, **process_data))

    if processes and pid:
        # filter processes by PID
        pid = int(pid)
        assert pid > 0
        processes = processes.with_attributes(pid=pid)

    if processes and command is not None:
        # filter processes by command
        command = re.compile(command)
        processes = tobiko.select(process
                                  for process in processes
                                  if command.match(process.command))

    if processes and is_kernel is not None:
        # filter kernel processes
        processes = processes.with_attributes(is_kernel=bool(is_kernel))

    return processes


def wait_for_processes(timeout=float('inf'), sleep_interval=5.,
                       ssh_client=None, **list_params):
    start_time = time.time()
    time_left = timeout
    while True:
        processes = list_processes(timeout=time_left,
                                   ssh_client=ssh_client,
                                   **list_params)
        if not processes:
            break

        time_left = timeout - (time.time() - start_time)
        if time_left < sleep_interval:
            hostname = _hostname.get_hostname(ssh_client=ssh_client)
            process_lines = [
                '    {pid} {command}'.format(pid=process.pid,
                                             command=process.command)
                for process in processes]
            raise PsWaitTimeout(timeout=timeout, hostname=hostname,
                                processes='\n'.join(process_lines))

        time.sleep(sleep_interval)


def parse_pid(value):
    return 'pid', int(value)


def parse_command(value):
    return 'command', str(value)


PS_TABLE_SCHEMA = {
    'pid': parse_pid,
    'cmd': parse_command,
    'command': parse_command,
}


def parse_table(lines, schema, header_line=None):
    lines = iter(lines)
    while not header_line:
        header_line = next(lines)

    getters = []
    column_names = header_line.strip().lower().split()
    for position, name in enumerate(column_names):
        getter = schema.get(name)
        if getter:
            getters.append((position, getter))

    for line in lines:
        row = line.strip().split()
        if row:
            yield dict(getter(row[position])
                       for position, getter in getters)
