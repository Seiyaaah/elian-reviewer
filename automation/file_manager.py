import json
from pathlib import Path


class FileManager:
    """
    Handles reading and writing generated JSON files.
    """

    def __init__(self, output_folder: str):
        self.output_dir = Path(output_folder)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _write(self, path: Path, data):
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"Saved: {path}")

    def _read(self, path: Path):
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _subject_dir(self, subject_id: str) -> Path:
        path = self.output_dir / subject_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    # --------------------------------------------------
    # Subjects
    # --------------------------------------------------

    def save_subjects(self, data):
        self._write(
            self.output_dir / "subjects.json",
            data,
        )

    def load_subjects(self):
        return self._read(
            self.output_dir / "subjects.json",
        )

    # --------------------------------------------------
    # Lesson
    # --------------------------------------------------

    def save_lesson(self, subject_id: str, data):
        self._write(
            self._subject_dir(subject_id) / "lesson.json",
            data,
        )

    def load_lesson(self, subject_id: str):
        return self._read(
            self._subject_dir(subject_id) / "lesson.json",
        )

    # --------------------------------------------------
    # Notes
    # --------------------------------------------------

    def save_notes(self, subject_id: str, data):
        self._write(
            self._subject_dir(subject_id) / "notes.json",
            data,
        )

    def load_notes(self, subject_id: str):
        return self._read(
            self._subject_dir(subject_id) / "notes.json",
        )

    # --------------------------------------------------
    # Questions
    # --------------------------------------------------

    def save_questions(self, subject_id: str, data):
        self._write(
            self._subject_dir(subject_id) / "questions.json",
            data,
        )

    def load_questions(self, subject_id: str):
        return self._read(
            self._subject_dir(subject_id) / "questions.json",
        )