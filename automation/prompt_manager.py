from pathlib import Path


class PromptManager:
    def __init__(self):
        root = Path(__file__).parent.parent

        self.prompt_dir = root / "prompts"
        self.schema_dir = root / "schemas"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _load(self, filename: str) -> str:
        path = self.prompt_dir / filename

        if not path.exists():
            raise FileNotFoundError(path)

        return path.read_text(encoding="utf-8")

    def _schema(self, filename: str) -> str:
        path = self.schema_dir / filename

        if not path.exists():
            raise FileNotFoundError(path)

        return path.read_text(encoding="utf-8")

    def _build(
        self,
        prompt_file: str,
        schema_file: str,
        **kwargs,
    ) -> str:
        prompt = self._load(prompt_file)
        schema = self._schema(schema_file)

        prompt = prompt.replace(
            "{{JSON_SCHEMA}}",
            schema,
        )

        for key, value in kwargs.items():
            prompt = prompt.replace(
                "{{" + key.upper() + "}}",
                str(value),
            )

        return prompt

    # --------------------------------------------------
    # Subjects
    # --------------------------------------------------

    def subject_prompt(
        self,
        subject_count: int,
    ):
        return self._build(
            "subjects.txt",
            "subjects.json",
            subject_count=subject_count,
        )

    # --------------------------------------------------
    # Lesson
    # --------------------------------------------------

    def lesson_prompt(
        self,
        subject_id: str,
    ):
        return self._build(
            "lesson.txt",
            "lesson.json",
            subject_id=subject_id,
        )
    # --------------------------------------------------
    # Lesson
    # --------------------------------------------------

    def notes_prompt(
        self,
        subject_id,
        subject_title,
    ):
        return self._build(
            "notes.txt",
            "notes.json",
            subject_id=subject_id,
            subject_title=subject_title,
        )

    # --------------------------------------------------
    # Questions
    # --------------------------------------------------

    def question_prompt(
        self,
        subject_id: str,
        question_types,
        question_count,
    ):
        return self._build(
            "questions.txt",
            "questions.json",
            subject_id=subject_id,
            question_types=", ".join(question_types),
            question_count=question_count,
        )
    