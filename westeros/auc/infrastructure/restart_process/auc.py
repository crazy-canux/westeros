from robot.api import logger

from super_devops.robotframework.unittest_wrapper import BaseUnitTest
from super_devops.ssh.paramiko_wrapper import BaseParamiko


class RestartProcessAUC(BaseUnitTest):
    def __init__(self, keyword, host, username, password, sudo_pw, process):
        super(RestartProcessAUC, self).__init__(
            keyword,
            method_name='test_restart'
        )
        self._host = host
        self._username = username
        self._password = password

        self._sudo_pw = sudo_pw
        self._process = process

        self._output = None

    def test_restart(self):
        cmd = "sudo service {} restart".format(self._process)
        logger.debug("cmd: {}".format(cmd))
        with BaseParamiko(
                self._host, self._username, self._password
        ) as ssh:
            output, error, rc = ssh.exec_command(
                cmd, get_pty=True, sudo_pw=self._sudo_pw
            )
            # TODO: validate result.
        # TODO: validate process started.
        import time
        time.sleep(5)

    def _validate_input(self):
        assert self._host is not None, 'Host is required.'
        assert self._username is not None, 'username is required.'
        assert self._password is not None, 'password is required.'
        assert self._sudo_pw is not None, 'sudo password is required.'
        assert self._process is not None, 'process is required.'