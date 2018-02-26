from .open.auc import OpenAUC
from .close.auc import CloseAUC


class BrowserManager(object):
    _INSTANCES = {}

    def __init__(self, keyword, browser_id, browser_type):
        self._keyword = keyword
        self._browser_id = browser_id
        self._browser_type = browser_type

    @staticmethod
    def get_browser_by_id(browser_id):
        return BrowserManager._INSTANCES.get(browser_id)

    @property
    def current_browser(self):
        return self._INSTANCES.get(self._browser_id)

    def open(self, headless_mode, url):
        _id, _driver = OpenAUC(
            self._keyword,
            self._browser_id, self._browser_type,
            headless_mode, url
        ).run()
        _browser_id, BrowserManager._INSTANCES[_browser_id] = _id, _driver
        return _browser_id

    def close(self, browser_id=None):
        _instance = BrowserManager._INSTANCES.pop(
            browser_id or self._browser_id, None
        )
        CloseAUC(self._keyword, _instance).run()
