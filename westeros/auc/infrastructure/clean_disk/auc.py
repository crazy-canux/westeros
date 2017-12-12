from robot.api import logger

from super_devops.unittest.unittest_wrapper import BaseUnitTest
from super_devops.ssh.paramiko_wrapper import BaseParamiko


class CleanDiskAUC(BaseUnitTest):
    def __init__(self, keyword, host, username, password, sudo_pw, path):
        super(CleanDiskAUC, self).__init__(keyword, method_name='test_clean')

        self._host = host
        self._username = username
        self._password = password

        self._sudo_pw = sudo_pw
        self._path = path

        self._output = None

    def test_clean(self):
        cmd = "sudo /bin/rm -rf {}".format(self._path)
        logger.debug("cmd: {}".format(cmd))
        with BaseParamiko(
                self._host, self._username, self._password,
        ) as ssh:
            self._output = ssh.exec_command(
                cmd, get_pty=True, sudo_pw=self._sudo_pw
            )
            logger.debug("output: {}".format(self._output))
        # TODO: validate result.

    def _validate_input(self):
        assert self._host is not None, "Host is required."
        assert self._username is not None, "Username is required."
        assert self._password is not None, "Password is required."
        assert self._sudo_pw is not None, 'sudo password is required.'
        assert self._path is not None, 'disk path is required.'

    def _validate_output(self):
        return self._output
