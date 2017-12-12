from .login.auc import LoginAUC
from .logout.auc import LogoutAUC


class AuthManager(object):
    CURRENT_USER = None

    def __init__(self, keyword):
        self._keyword = keyword

    def login(self, username, password):
        _already_logged_in = LoginAUC(
            self._keyword, username, password
        ).run()
        if _already_logged_in:
            AuthManager.CURRENT_USER = username
        return _already_logged_in

    def logout(self):
        LogoutAUC(self._keyword, AuthManager.CURRENT_USER).run()
        AuthManager.CURRENT_USER = None
