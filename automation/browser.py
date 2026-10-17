from playwright.sync_api import sync_playwright


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()