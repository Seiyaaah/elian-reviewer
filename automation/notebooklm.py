from playwright.sync_api import Page


class NotebookLM:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(
            "https://notebooklm.google.com",
            wait_until="networkidle",
        )

    def create_notebook(self):
        print("Looking for New notebook button...")

        self.page.get_by_role(
            "button",
            name="New notebook",
        ).click()

        print("Clicked button.")

        # Wait until NotebookLM changes to the notebook page
        self.page.wait_for_url("**/notebook/**")

        # Wait until the URL is no longer ".../creating"
        self.page.wait_for_function(
            "() => !window.location.pathname.endsWith('/creating')"
        )

        # Wait for the page to finish rendering
        self.page.wait_for_load_state("networkidle")

        print("Current URL:", self.page.url)
        print("Notebook page loaded.")

    def open_sources(self):
        print("Opening Sources...")

        self.page.get_by_text(
            "Sources",
            exact=True,
        ).click()

        print("Sources opened.")

    def click_add_sources(self):
        print("Clicking Add sources...")

        self.page.get_by_role(
            "button",
            name="Add source",
        ).click()

        print("Add sources dialog opened.")

    def upload_files(self):
        print("Clicking Upload files...")

        self.page.get_by_text(
            "Upload files",
            exact=False,
        ).click()

        print("Upload dialog opened.")

    def upload_source_files(self, files):
        print("Uploading files...")

        file_input = self.page.locator("input[type='file']")
        file_input.set_input_files(files)

        print("Files uploaded!")

    def debug_buttons(self):
        print("\n=== BUTTONS ON CURRENT PAGE ===")

        buttons = self.page.locator("button")
        count = buttons.count()

        for i in range(count):
            try:
                btn = buttons.nth(i)

                print(
                    f"{i}:",
                    "aria-label =", btn.get_attribute("aria-label", timeout=1000),
                    "| text =", btn.text_content(timeout=1000),
                )
            except Exception as e:
                print(f"{i}: <button disappeared> ({e.__class__.__name__})")

    def debug_text(self, text):
        locator = self.page.get_by_text(text, exact=False)
        print(f"'{text}': {locator.count()} matches")