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

import typing  # noqa

import tobiko
from tobiko.shell import sh
from tobiko.shell import ssh


class NoMatchingLinesFound(tobiko.TobikoException):
    message = ("No matching lines found in files (pattern='{pattern}',"
               " files={files}, login={login})")


def grep(pattern: str,
         command: typing.Optional[sh.ShellCommandType] = None,
         grep_command: sh.ShellCommandType = 'zgrep -Eh',
         files: typing.Optional[typing.List[str]] = None,
         ssh_client: ssh.SSHClientFixture = None,
         blank_lines: bool = True,
         **execute_params) -> typing.List[str]:
    if not pattern:
        raise ValueError("Pattern string can't be empty")
    if command:
        if files:
            raise ValueError("File list must be empty when command is given")
        command_line = sh.shell_command(command) + ['|'] + grep_command + [
            '-e', pattern]
    elif files:
        command_line = sh.shell_command(grep_command) + [
            '-e', pattern] + files
    else:
        raise ValueError("command and files can't be both empty or None")

    try:
        result = sh.execute(command_line,
                            ssh_client=ssh_client,
                            **execute_params)
    except sh.ShellCommandFailed as ex:
        if ex.exit_status > 1:
            # Some unknown problem occurred
            raise
    else:
        output_lines: typing.List[str] = [
            line
            for line in result.stdout.splitlines()
            if blank_lines or line.strip()]
        if output_lines:
            return output_lines
    raise NoMatchingLinesFound(pattern=pattern,
                               files=files,
                               login=ssh_client and ssh_client.login or None)


def grep_files(pattern: str,
               files: typing.List[str],
               **grep_params) -> typing.List[str]:
    return grep(pattern=pattern, files=files, **grep_params)


def grep_lines(pattern: str,
               command: sh.ShellCommandType,
               **grep_params) -> typing.List[str]:
    return grep(pattern=pattern, command=command, **grep_params)
