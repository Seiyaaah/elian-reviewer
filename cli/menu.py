import questionary
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from models.reviewer_config import ReviewerConfig

from cli.picker import (
    pick_source_files,
    pick_output_folder,
)

console = Console()


def positive_integer(text: str):
    return (
        text.isdigit() and int(text) > 0
    ) or "Please enter a positive whole number."


def run_cli():
    console.print(
        Panel.fit(
            "[bold cyan]Elian Reviewer[/bold cyan]\nNotebookLM Automation",
            title="Welcome",
        )
    )

    # -----------------------------
    # Subject Count
    # -----------------------------
    subject_count = int(
        questionary.text(
            "How many subjects should be generated?",
            default="1",
            validate=positive_integer,
        ).ask()
    )

    # -----------------------------
    # Question Types
    # -----------------------------
    question_types = questionary.checkbox(
        "Select question types",
        choices=[
            questionary.Choice("Multiple Choice"),
            questionary.Choice("True or False"),
            questionary.Choice("Modified True or False"),
            questionary.Choice("Identification"),
            questionary.Choice("Enumeration"),
        ],
        validate=lambda selected: (
            True if selected else "Please select at least one question type."
        ),
    ).ask()

    # -----------------------------
    # Number of Questions
    # -----------------------------
    question_count = int(
        questionary.text(
            "How many questions should be generated?",
            default="20",
            validate=positive_integer,
        ).ask()
    )

    # -----------------------------
    # Source Files
    # -----------------------------
    console.print()
    console.print("[cyan]Select your study materials...[/cyan]")

    source_files = pick_source_files()

    # -----------------------------
    # Output Folder
    # -----------------------------
    console.print()
    console.print("[cyan]Select your output repository...[/cyan]")

    output_folder = pick_output_folder()

    # -----------------------------
    # Summary
    # -----------------------------
    console.print()
    console.print(Rule("[bold blue]Configuration Summary"))

    console.print(f"[green]Subjects to Generate:[/green] {subject_count}")
    console.print(f"[green]Question Types:[/green] {', '.join(question_types)}")
    console.print(f"[green]Questions per Subject:[/green] {question_count}")

    console.print("\n[bold green]Selected Source Files[/bold green]")
    for file in source_files:
        console.print(f" • {file}")

    console.print("\n[bold green]Output Repository[/bold green]")
    console.print(output_folder)

    console.print()

    if not questionary.confirm(
        "Start generation?",
        default=True,
    ).ask():
        raise KeyboardInterrupt("Operation cancelled by user.")

    return ReviewerConfig(
        subject_count=subject_count,
        question_types=question_types,
        question_count=question_count,
        source_files=source_files,
        output_folder=output_folder,
    )