from cli.menu import run_cli
from automation.browser import BrowserManager
from models.reviewer_config import ReviewerConfig


def main():
    config = run_cli()

    browser = BrowserManager()

    browser.start()

    print("Browser Manager Started!")

    browser.close()

    print("Browser Closed!")


if __name__ == "__main__":
    main()