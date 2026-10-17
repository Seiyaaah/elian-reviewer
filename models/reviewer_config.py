from pydantic import BaseModel


class ReviewerConfig(BaseModel):
    question_type: str
    question_count: str
    source_files: list[str]
    output_folder: str