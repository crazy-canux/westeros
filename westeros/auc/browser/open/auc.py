from super_devops.robotframework.unittest_wrapper import BaseUnitTest
from super_devops.selenium.selenium_wrapper import BaseSelenium


class OpenAUC(BaseUnitTest):
    def __init__(self, keyword, browser_id, browser_type, headless_mode, url):
        super(OpenAUC, self).__init__(keyword, method_name='test_open_browser')

        self.browser_id = browser_id
        self.browser_type = browser_type
        self.headless_mode = headless_mode
        self.url = url

        self.browser = None

    def test_open_browser(self):
        self.browser = BaseSelenium(
            self.browser_id, self.browser_type, self.headless_mode
        )
        self.browser.launch(self.url)
        self.browser.maximize_window()

    def _validate_input(self):
        assert self.browser_id is not None, "Browser identifier is required."
        assert self.browser_type is not None, "Browser type is required."
        assert self.url is not None, "URL is required."

    def _validate_output(self):
        return self.browser_id, self.browser
