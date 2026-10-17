from cli.menu import run_cli
from automation.browser import BrowserManager
from automation.notebooklm import NotebookLM


def main():
    # Get user configuration
    config = run_cli()

    # Connect to Chrome
    browser = BrowserManager()
    browser.start()
    print("✅ Connected to Chrome")

    try:
        notebook = NotebookLM(browser.page)

        # ----------------------------
        # Open NotebookLM
        # ----------------------------
        print("\n🌐 Opening NotebookLM...")
        notebook.open()
        print("✅ NotebookLM opened")

        # ----------------------------
        # Create notebook
        # ----------------------------
        print("\n📔 Creating notebook...")
        notebook.create_notebook()
        print("✅ Notebook created")

        # ----------------------------
        # Add sources
        # ----------------------------
        print("\n📂 Opening Sources...")
        notebook.open_sources()

        print("➕ Opening Add Sources...")
        notebook.click_add_sources()

        print("📤 Uploading source files...")
        notebook.upload_files()
        notebook.upload_source_files(config.source_files)
        print("✅ Source files uploaded")

        # ----------------------------
        # Debug (temporary)
        # ----------------------------
        # notebook.debug_buttons()

        print("\nConfiguration:")
        print(config.model_dump())

        input("\nPress Enter to close...")

    finally:
        browser.close()
        print("👋 Browser disconnected")


if __name__ == "__main__":
    main()