

class DbManager(object):

    """All database related auc."""

    def __init__(self, keyword, host, port, username, password, database):
        self._keyword = keyword
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._database = database

