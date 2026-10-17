from models.reviewer_config import ReviewerConfig
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from cli.picker import (
    pick_source_files,
    pick_output_folder,
)

console = Console()


def run_cli():
    console.print(
        Panel.fit(
            "[bold cyan]Elian Reviewer[/bold cyan]\nNotebookLM Automation",
            title="Welcome",
        )
    )

    # -----------------------------
    # Question Type
    # -----------------------------
    question_type = questionary.select(
        "Select Question Type",
        choices=[
            "Multiple Choice",
            "True or False",
            "Modified True or False",
            "Identification",
            "Enumeration",
            "Mixed",
        ],
    ).ask()

    # -----------------------------
    # Number of Questions
    # -----------------------------
    question_count = questionary.text(
        "Number of Questions (Leave blank for maximum):"
    ).ask()

    if not question_count:
        question_count = "Maximum"

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

    console.print(f"[green]Question Type:[/green] {question_type}")
    console.print(f"[green]Questions:[/green] {question_count}")

    console.print("\n[bold green]Selected Source Files[/bold green]")

    for file in source_files:
        console.print(f" • {file}")

    console.print(f"\n[bold green]Output Repository[/bold green]")
    console.print(output_folder)

    # -----------------------------
    # Return Configuration
    # -----------------------------
    return ReviewerConfig(
        question_type=question_type,
        question_count=question_count,
        source_files=source_files,
        output_folder=output_folder,
    )