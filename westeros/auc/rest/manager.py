

class RestManager(object):

    """All restful api related auc."""

    def __init__(self, keyword, username, password, domain, url):
        self._keyword = keyword
        self._username = username
        self._password = password
        self._domain = domain
        self._url = url

