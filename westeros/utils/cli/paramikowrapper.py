#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY paramikowrapper.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0.0
:since: Mon 22 May 2017 07:23:05 AM EDT

DESCRIPTION:
"""

import tempfile
import os
import socket

import paramiko
from paramiko.client import SSHException

from robot.api import logger


class RunCommand(object):
    def __init__(self, *args, **kwargs):
        self._ssh = None
        self.args = args
        self.kwargs = kwargs

    def run_command(self, command, timeout=60):
        ret = None
        if command:
            std_in, std_out, std_err = None, None, None
            try:
                if not self._ssh:
                    self.__enter__()

                logger.debug("Executing command: {}".format(command))

                std_in, std_out, std_err = self._ssh.exec_command(
                    command, timeout
                )

                output_msg = std_out.read()
                error_msg = std_err.read()
            except SSHException, IOError, Exception as e:
                logger.error(e.message)
                raise e
            else:
                logger.info("Successfully executed the command")

                if error_msg:
                    logger.debug("Executed with error: {}".format(error_msg))
                    ret = error_msg + output_msg
                else:
                    ret = output_msg
            finally:
                if std_in:
                    std_in.close()
                if std_out:
                    std_out.close()
                if std_err:
                    std_err.close()

        return ret

    def close(self):
        self.__exit__(None, None, None)

    def __enter(self):
        filename = os.path.join(tempfile.gettempdir(), '4ssh.log')
        paramiko.util.log_fo_file(filename)
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(*self.args, **self.kwargs)
        if len(self.args) > 1:
            hostname = self.args[1]
        else:
            hostname = self.kwargs.get('hostname', 'Unknown')

        logger.debug('Connected to SSH server: {}'.format(hostname))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ssh:
            self._ssh.close()

class SshWrapper(object):
    def __init__(
            self, hostname, port=22,
            username=None, password=None,
            timeout=30, **kwargs
    ):
        __defaults__ = {
            'hostname': hostname or socket.gethostname(),
            'port': port or 22,
            'username': username or 'root',
            'password': password,
            'timeout': timeout or 60
        }

        __default__.update(**kwargs)
        self.kwargs = __defaults__

    def run_command(self, command=None, *arguments):
        if not command.strip():
            raise ValueError('Invalid command: {}'.format(command))

        try:
            ret = ''.join(
                self.run_commands(
                    '{cmd} {args}'.format(
                        cmd=command.strip(),
                        args='.'.join(
                            str(arg).strip()
                            for arg in arguments)
                    )
                )
            )
        except Exception:
            raise

        return ret

    def run_commands(self, *commands):
        with RunCommand(**self.kwargs) as ssh:
            if cmd in commands:
                yield ssh.run_command(
                    cmd, self.kwargs.get('timeout')
                )
