import os

from westeros.auc.browser.manager import BrowserManager
from westeros.auc.authentication.manager import AuthManager
from westeros.auc.dashboard.manager import DashboardManager
from .base_workflow import BaseWorkflow


class BrowserWorkflow(BaseWorkflow):

    def open_browser_on_westeros_ui(
            self,
            browser_id='westeros',
            browser_type=None,
            url=None
    ):
        try:
            if not browser_type:
                browser_type = self.ctx.Browser["browser_type"]

            headless_mode = self.ctx.Browser["headless_mode"]

            url = url or self.ctx.WesterosWeb['url'] or 'about:blank'

            browser_id = BrowserManager(
                self.open_browser_on_westeros_ui.__name__,
                browser_id, browser_type
            ).open(headless_mode, url)
        except Exception:
            raise
        else:
            self.ctx.shared += dict(
                browser=dict(id=browser_id)
            )
        return browser_id

    def close_browser(
            self,
            browser_id=None,
            browser_type=None
    ):
        try:
            if not browser_type:
                browser_type = self.ctx.Browser["browser_type"]

            browser_id = self.ctx.browser['id']

            BrowserManager(
                self.close_browser.__name__, browser_id, browser_type
            ).close(
                browser_id
            )
        except Exception:
            raise
        finally:
            if self.ctx.browser['id']:
                self.ctx.shared.browser['id'] = None

    def user_login_in_to_westeros_ui(self, username=None, password=None):
        try:
            if not username:
                username = self.ctx.WesterosWeb['username']
                password = self.ctx.WesterosWeb['password']
            if AuthManager.CURRENT_USER:
                if AuthManager.CURRENT_USER.lower() != username.lower():
                    self.user_logout_from_westeros_ui(AuthManager.CURRENT_USER)
            already_logged_in = AuthManager(
                "user({})_login_to_westeros_ui".format(username)
            ).login(username, password)
        except Exception:
            raise
        else:
            self.ctx.shared['westeros_user'] = AuthManager.CURRENT_USER
        return already_logged_in

    def user_logout_from_westeros_ui(self, username=None):
        try:
            username = AuthManager.CURRENT_USER
            AuthManager(
                "user({}) logout from dashboard submit_via_rest".format(username)
            ).logout()
        except Exception:
            raise
        else:
            self.ctx.shared.westeros_user = None
