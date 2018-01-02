from super_devops.robotframework.unittest_wrapper import BaseUnitTest

from westeros.utils.dashboard import Dashboard


class LoginAUC(BaseUnitTest):
    def __init__(self, keyword, username, password):
        super(LoginAUC, self).__init__(keyword, method_name='test_login')

        self.username = username
        self.password = password
        self.already_logged_in = False

        self.dashboard = Dashboard()

    def test_login(self):
        self.dashboard.username_textbox.set(self.username)
        self.dashboard.password_textbox.set(self.password)

        self.assertTrue(
            self.dashboard.login_button.enabled,
            msg='Login button not enabled.'
        )
        self.dashboard.login_button.click()

        self.already_logged_in = self.dashboard.logout_button.enabled

        self.assertTrue(
            self.already_logged_in,
            msg='Login to dashboard UI failed.'
        )

    def _validate_input(self):
        assert self.username is not None, 'Username is required.'
        assert self.password is not None, 'Password is required.'

    def _validate_output(self):
        return self.already_logged_in





