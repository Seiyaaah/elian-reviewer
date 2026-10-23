from automation.prompt_manager import PromptManager
from automation.response_parser import ResponseParser
from automation.file_manager import FileManager
from automation.notebooklm import NotebookLM


class ReviewPipeline:
    def __init__(self, notebook: NotebookLM, config):
        self.notebook = notebook
        self.config = config

        self.prompts = PromptManager()
        self.parser = ResponseParser()
        self.files = FileManager(config.output_folder)

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def _get_subject_id(self, subject: dict) -> str:
        subject_id = ResponseParser.get_subject_id(subject)

        if not subject_id:
            raise ValueError(f"Subject has no id:\n{subject}")

        return subject_id

    def _get_response(self) -> str:
        response = self.notebook.get_last_response()

        if response is None:
            raise RuntimeError("NotebookLM returned None.")

        response = response.strip()

        if not response:
            raise RuntimeError("NotebookLM returned an empty response.")

        return response

    # --------------------------------------------------
    # Pipeline
    # --------------------------------------------------

    async def run(self):
        print("\n========== REVIEW PIPELINE ==========\n")

        await self.generate_subjects()

        subjects = self.files.load_subjects()

        if not subjects:
            raise RuntimeError("No subjects were generated.")

        for subject in subjects:
            await self.generate_lesson(subject)
            await self.generate_notes(subject)
            await self.generate_questions(subject)

        print("\n========== PIPELINE COMPLETE ==========\n")

    # --------------------------------------------------
    # Subjects
    # --------------------------------------------------

    async def generate_subjects(self):
        print("\nGenerating Subjects...")

        prompt = self.prompts.subject_prompt(
            subject_count=self.config.subject_count
        )

        await self.notebook.send_prompt(prompt)

        response = self._get_response()

        subjects = self.parser.parse_subjects(response)

        expected = self.config.subject_count

        if len(subjects) != expected:
            raise ValueError(
                f"Expected {expected} subjects but received {len(subjects)}."
            )

        self.files.save_subjects(subjects)

        print(f"✓ Saved {len(subjects)} subjects.")

    # --------------------------------------------------
    # Lesson
    # --------------------------------------------------

    async def generate_lesson(self, subject):
        subject_id = self._get_subject_id(subject)

        print(f"\nGenerating Lesson: {subject_id}")

        prompt = self.prompts.lesson_prompt(
            subject_id=subject_id
        )

        await self.notebook.send_prompt(prompt)

        response = self._get_response()

        lesson = self.parser.parse_lessons(response)

        self.files.save_lesson(
            subject_id,
            lesson,
        )

        print("✓ Lesson saved.")

    # --------------------------------------------------
    # Notes
    # --------------------------------------------------

    async def generate_notes(self, subject):
        subject_id = self._get_subject_id(subject)

        print(f"\nGenerating Notes: {subject_id}")

        prompt = self.prompts.notes_prompt(
            subject_id=subject_id,
            subject_title=subject["title"],
        )

        await self.notebook.send_prompt(prompt)

        response = self._get_response()

        # DEBUG: Print the raw NotebookLM response
        print("\n========== RAW NOTEBOOKLM RESPONSE ==========\n")
        print(response)
        print("\n=============================================\n")

        notes = self.parser.parse_notes(response)

        self.files.save_notes(
            subject_id,
            notes,
        )

        print("✓ Notes saved.")

    # --------------------------------------------------
    # Questions
    # --------------------------------------------------

    async def generate_questions(self, subject):
        subject_id = self._get_subject_id(subject)

        print(f"\nGenerating Questions: {subject_id}")

        prompt = self.prompts.question_prompt(
            subject_id=subject_id,
            question_types=self.config.question_types,
            question_count=self.config.question_count,
        )

        await self.notebook.send_prompt(prompt)

        response = self._get_response()

        questions = self.parser.parse_questions(response)

        self.files.save_questions(
            subject_id,
            questions,
        )

        print("✓ Questions saved.")