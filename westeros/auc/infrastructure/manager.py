from .clean_disk.auc import CleanDiskAUC
from .restart_process.auc import RestartProcessAUC


class InfraManager(object):

    """Include storage/virtualization/network."""

    def __init__(self, keyword, host, username, password, sudo_pw):
        self._keyword = keyword
        self._host = host
        self._username = username
        self._password = password
        self._sudo_pw = sudo_pw

    def clean_disk(self, path):
        CleanDiskAUC(
            self._keyword, self._host, self._username, self._password,
            self._sudo_pw, path
        ).run()

    def restart_process(self, process):
        RestartProcessAUC(
            self._keyword, self._host, self._username, self._password,
            self._sudo_pw, process
        ).run()
