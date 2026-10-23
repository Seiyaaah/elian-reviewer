import asyncio
import traceback

from cli.menu import run_cli

from automation.notebooklm import NotebookLM
from automation.pipeline import ReviewPipeline


async def main(config):
    notebook = NotebookLM()

    try:
        # --------------------------------------------------
        # Connect
        # --------------------------------------------------

        print("\n🔐 Connecting to NotebookLM...")
        await notebook.connect()
        print("✅ Connected")

        # --------------------------------------------------
        # Create Notebook
        # --------------------------------------------------

        print("\n📔 Creating notebook...")
        await notebook.create_notebook("Reviewer")
        print("✅ Notebook created")

        # --------------------------------------------------
        # Upload Sources
        # --------------------------------------------------

        print("\n📤 Uploading source files...")
        await notebook.upload_source_files(config.source_files)
        print("✅ Upload complete")

        # --------------------------------------------------
        # Pipeline
        # --------------------------------------------------

        print("\n🚀 Starting Review Pipeline...")

        pipeline = ReviewPipeline(
            notebook=notebook,
            config=config,
        )

        await pipeline.run()

        print("\n🎉 Review generation completed!")

    except Exception as e:
        print("\n❌ Pipeline failed!")
        print(f"\n{type(e).__name__}: {e}\n")
        traceback.print_exc()

    finally:
        try:
            await notebook.close()
        except Exception:
            pass

        print("\n👋 Disconnected")


if __name__ == "__main__":
    config = run_cli()
    asyncio.run(main(config))