from pathlib import Path
from notebooklm import NotebookLMClient


class NotebookLM:
    def __init__(self):
        self.client = None
        self.notebook = None
        self.last_response = None
        self._ctx = None

    # --------------------------------------------------
    # Connection
    # --------------------------------------------------

    async def connect(self):
        self._ctx = NotebookLMClient.from_storage()
        self.client = await self._ctx.__aenter__()

    async def close(self):
        if self._ctx:
            await self._ctx.__aexit__(None, None, None)

    # --------------------------------------------------
    # Notebook
    # --------------------------------------------------

    async def create_notebook(self, title="Reviewer"):
        print(f"Creating notebook: {title}")
        self.notebook = await self.client.notebooks.create(title)

    # --------------------------------------------------
    # Sources
    # --------------------------------------------------

    async def upload_source_files(self, files):
        for file in files:
            print(f"Uploading {Path(file).name}...")

            await self.client.sources.add_file(
                self.notebook.id,
                file,
                wait=True,
            )

    # --------------------------------------------------
    # Chat
    # --------------------------------------------------

    async def send_prompt(self, prompt):
        print("Sending prompt...")

        result = await self.client.chat.ask(
            self.notebook.id,
            prompt,
        )

        self.last_response = result.answer or ""

        # ---------- DEBUG ----------
        print("\n========== RAW NOTEBOOKLM RESPONSE ==========")
        print(self.last_response)
        print("=============================================\n")

        with open(
            "last_notebooklm_response.txt",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.last_response)

    async def wait_for_response(self):
        pass

    # --------------------------------------------------
    # Response
    # --------------------------------------------------

    def get_last_response(self):
        return self.last_response