from playwright.sync_api import sync_playwright


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.connect_over_cdp(
            "http://127.0.0.1:9222"
        )

        self.context = self.browser.contexts[0]

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

    def close(self):
        if self.playwright:
            self.playwright.stop()