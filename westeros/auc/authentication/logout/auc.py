from super_devops.robotframework.unittest_wrapper import BaseUnitTest

from westeros.utils.dashboard import Dashboard


class LogoutAUC(BaseUnitTest):
    def __init__(self, keyword, username):
        super(LogoutAUC, self).__init__(keyword, method_name='test_logout')
        self.username = username

        self.dashboard = Dashboard()

    def test_logout(self):
        self.assertTrue(
            self.dashboard.logout_button.enabled,
            'logout from dashboard ui failed.'
        )
        self.dashboard.logout_button.click()
        import time
        time.sleep(1)

        self.assertTrue(
            self.dashboard.login_button.enabled,
            'logout finished, bug reload login page failed.'
        )

    def _validate_input(self):
        assert self.username is not None, 'Username is required.'
