from super_devops.robotframework.unittest_wrapper import BaseUnitTest
from super_devops.selenium.selenium_wrapper import BaseSelenium


class CloseAUC(BaseUnitTest):
    def __init__(self, keyword, instance):
        super(CloseAUC, self).__init__(
            keyword,
            method_name='test_close_browser'
        )
        self.browser = instance

    def test_close_browser(self):
        if self.browser:
            self.browser.close()

    def _validate_input(self):
        assert isinstance(self.browser, BaseSelenium), 'Invalid browser.'

