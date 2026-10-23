# VoiLearn Automation TODO

## Goal

Automatically convert one or more learning resources into VoiLearn JSON files with zero manual editing.

---

# Requirements

## Software

- [ ] Python 3.11+
- [ ] Google Chrome
- [ ] NotebookLM CLI
- [ ] Git
- [ ] Virtual Environment (recommended)

---

# Authentication

- [ ] Install NotebookLM CLI
- [ ] Login using Chrome
- [ ] Verify the CLI can create notebooks
- [ ] Verify the CLI can upload files
- [ ] Verify the CLI can send prompts
- [ ] Verify the CLI can receive responses

---

# Project Structure

automation/

    input/
        Subject A/
        Subject B/
        Subject C/

    prompts/
        subjects.txt
        lessons.txt
        notes.txt
        questions.txt

    schemas/
        subjects.json
        lessons.json
        notes.json
        questions.json

    output/

    parser/

    run.py

---

# Workflow

For every folder inside input/

1. Detect subject folder

2. Create NotebookLM notebook

3. Upload every file inside the folder

4. Wait until NotebookLM finishes indexing

5. Generate Subjects JSON

6. Validate Subjects JSON

7. Generate Lessons JSON

8. Validate Lessons JSON

9. Generate Notes JSON

10. Validate Notes JSON

11. Generate Questions JSON

12. Validate Questions JSON

13. Save all JSON files

14. Move to next subject

---

# Input

Each folder represents ONE subject.

Example

input/

    Anatomy/
        Slides.pdf
        Reviewer.pdf
        Book.pdf
        Notes.docx

Everything inside the folder should be uploaded automatically.

No manual selection.

---

# NotebookLM Prompts

Generate:

- Subjects
- Lessons
- Notes
- Questions

Each prompt should use:

- Prompt Template
- JSON Schema
- Strict JSON output

---

# JSON Validation

Every NotebookLM response should go through

ResponseParser.clean()

↓

ResponseParser.parse()

↓

Validation

↓

Save

Never save invalid JSON.

---

# Supported Question Types

- Multiple Choice
- Identification
- Enumeration
- True / False
- Modified True / False

Future

- Matching
- Fill in the Blank
- Essay

---

# Multiple Sources

Support unlimited sources.

Example

Subject/

    Slides.pdf
    Reviewer.pdf
    Book.pdf
    Notes.docx
    Transcript.txt
    Handouts.pdf

Upload ALL files into the same NotebookLM notebook.

Generate ONE combined subject.

---

# Error Handling

If upload fails

→ Retry

If NotebookLM times out

→ Retry

If parser fails

→ Retry generation

If JSON is invalid

→ Reject and regenerate

Never overwrite existing JSON with invalid data.

---

# Output

Automatically generate

data/

    subjects.json

    lessons.json

    notes.json

    questions.json

No manual copying.

---

# Automation Features

- Automatic folder detection
- Automatic notebook creation
- Automatic file upload
- Automatic prompt execution
- Automatic JSON validation
- Automatic saving
- Automatic retry on failure
- Automatic processing of multiple subjects

---

# Future Improvements

- Progress bar
- Duplicate detection
- Watch Folder Mode
- Incremental updates
- OCR support
- Image extraction
- PDF compression
- Logging
- CLI dashboard
- Parallel processing

---

# Complete Pipeline

Drop Files

↓

Detect Subject Folder

↓

Create NotebookLM Notebook

↓

Upload All Sources

↓

Wait for Indexing

↓

Generate Subjects

↓

Validate

↓

Generate Lessons

↓

Validate

↓

Generate Notes

↓

Validate

↓

Generate Questions

↓

Validate

↓

Save JSON

↓

Process Next Subject

↓

Done
