from pathlib import Path

from pydantic import BaseModel


class ReviewerConfig(BaseModel):
    subject_count: int

    # Multiple selected question types
    question_types: list[str]
    question_count: int

    source_files: list[Path]
    output_folder: Path