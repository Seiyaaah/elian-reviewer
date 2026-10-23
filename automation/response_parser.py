import json
import re


class ResponseParser:
    """
    Cleans and parses NotebookLM JSON responses.
    """

    # --------------------------------------------------
    # Cleaning
    # --------------------------------------------------

    @staticmethod
    def clean(response: str) -> str:
        if not response:
            return ""

        response = response.strip()

        # Remove NotebookLM citations like [1], [2-4], [3,5]
        response = re.sub(r"\[\d+(?:[-,]\d+)*\]", "", response)

        # Prefer JSON inside Markdown code blocks
        match = re.search(
            r"```(?:json)?\s*(.*?)\s*```",
            response,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if match:
            return match.group(1).strip()

        # Otherwise locate the first JSON object or array
        object_pos = response.find("{")
        array_pos = response.find("[")

        positions = [p for p in (object_pos, array_pos) if p != -1]

        if not positions:
            raise ValueError("No JSON found in NotebookLM response.")

        return response[min(positions):].strip()

    # --------------------------------------------------
    # Generic Parser
    # --------------------------------------------------

    @classmethod
    def parse(cls, response: str):

        print("\n========== RAW RESPONSE ==========\n")
        print(response[:4000])

        if len(response) > 4000:
            print("\n... output truncated ...")

        print("\n==================================\n")

        cleaned = cls.clean(response)

        print("\n========== CLEANED JSON ==========\n")
        print(cleaned[:4000])

        if len(cleaned) > 4000:
            print("\n... output truncated ...")

        print("\n==================================\n")

        if not cleaned:
            raise ValueError("NotebookLM returned an empty response.")

        try:
            decoder = json.JSONDecoder()
            data, end = decoder.raw_decode(cleaned)

            # Warn if extra text exists after JSON
            extra = cleaned[end:].strip()

            if extra:
                print("\nWARNING: Extra text detected after JSON.")
                print(extra[:500])

            print("\n========== PARSED ==========")
            print("Type:", type(data).__name__)
            print("============================\n")

            return data

        except json.JSONDecodeError as e:

            lines = cleaned.splitlines()

            print("\n=========== JSON ERROR ===========")
            print(f"Line      : {e.lineno}")
            print(f"Column    : {e.colno}")
            print(f"Character : {e.pos}")
            print()

            if e.lineno > 1:
                print("Previous:")
                print(lines[e.lineno - 2])
                print()

            print("Error Line:")
            print(lines[e.lineno - 1])
            print(" " * (e.colno - 1) + "^")
            print()

            if e.lineno < len(lines):
                print("Next:")
                print(lines[e.lineno])
                print()

            start = max(0, e.pos - 200)
            end = min(len(cleaned), e.pos + 200)

            print("Nearby JSON:")
            print(cleaned[start:end])
            print("==================================")

            raise

    # --------------------------------------------------
    # Validation helpers
    # --------------------------------------------------

    @staticmethod
    def _validate_array(data, required_fields, name):

        if not isinstance(data, list):
            raise ValueError(f"{name} JSON must be a JSON array.")

        for i, item in enumerate(data):

            if not isinstance(item, dict):
                raise ValueError(
                    f"{name} at index {i} must be a JSON object, "
                    f"got {type(item).__name__}"
                )

            print(f"{name}[{i}] keys: {list(item.keys())}")

            missing = required_fields - item.keys()

            if missing:
                raise ValueError(
                    f"{name} at index {i} is missing required fields: "
                    f"{', '.join(sorted(missing))}"
                )

    # --------------------------------------------------
    # Subjects
    # --------------------------------------------------

    @classmethod
    def parse_subjects(cls, response: str):
        data = cls.parse(response)

        cls._validate_array(
            data,
            {"id", "title", "description"},
            "Subject",
        )

        return data

    # --------------------------------------------------
    # Lessons
    # --------------------------------------------------

    @classmethod
    def parse_lessons(cls, response: str):
        data = cls.parse(response)

        cls._validate_array(
            data,
            {
                "id",
                "subjectId",
                "title",
                "description",
                "content",
            },
            "Lesson",
        )

        return data

    # Alias
    parse_lesson = parse_lessons

    # --------------------------------------------------
    # Notes
    # --------------------------------------------------

    @classmethod
    def parse_notes(cls, response: str):
        data = cls.parse(response)

        cls._validate_array(
            data,
            {
                "id",
                "subjectId",
                "title",
                "summary",
                "sections",
            },
            "Note",
        )

        for note_index, note in enumerate(data):

            if not isinstance(note["sections"], list):
                raise ValueError(
                    f"Note {note_index}: sections must be a list."
                )

            for section_index, section in enumerate(note["sections"]):

                if not isinstance(section, dict):
                    raise ValueError(
                        f"Section {section_index} in note {note_index} must be a JSON object."
                    )

                required = {
                    "title",
                    "paragraphs",
                    "list",
                }

                missing = required - section.keys()

                if missing:
                    raise ValueError(
                        f"Section {section_index} in note {note_index} is missing: "
                        f"{', '.join(sorted(missing))}"
                    )

                if not isinstance(section["paragraphs"], list):
                    raise ValueError(
                        f"paragraphs in section {section_index} must be a list."
                    )

                if not isinstance(section["list"], list):
                    raise ValueError(
                        f"list in section {section_index} must be a list."
                    )

        return data

    # --------------------------------------------------
    # Questions
    # --------------------------------------------------

    @classmethod
    def parse_questions(cls, response: str):
        data = cls.parse(response)

        if not isinstance(data, list):
            raise ValueError(
                "Questions JSON must be a JSON array."
            )

        return data

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def get_subject_id(item: dict):
        return (
            item.get("subjectId")
            or item.get("subject_id")
            or item.get("id")
        )