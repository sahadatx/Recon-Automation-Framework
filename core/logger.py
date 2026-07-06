"""
Logger Module

Provides colorful logging utilities for the framework.
"""

from rich.console import Console
from rich.rule import Rule

console = Console()


# ==========================================================
# Basic Logs
# ==========================================================

def info(message: str) -> None:
    """Display an informational message."""
    console.print(
        f"[bold cyan][INFO][/bold cyan] {message}"
    )


def success(message: str) -> None:
    """Display a success message."""
    console.print(
        f"[bold green][SUCCESS][/bold green] {message}"
    )


def warning(message: str) -> None:
    """Display a warning message."""
    console.print(
        f"[bold yellow][WARNING][/bold yellow] {message}"
    )


def error(message: str) -> None:
    """Display an error message."""
    console.print(
        f"[bold red][ERROR][/bold red] {message}"
    )


def debug(message: str) -> None:
    """Display a debug message."""
    console.print(
        f"[bold magenta][DEBUG][/bold magenta] {message}"
    )


# ==========================================================
# Sections
# ==========================================================

def section(title: str) -> None:
    """
    Display a major section header.
    """

    console.print()
    console.print(
        Rule(
            title,
            style="bold bright_blue",
        )
    )


def subsection(title: str) -> None:
    """
    Display a subsection header.
    """

    console.print()
    console.print(
        Rule(
            title,
            style="cyan",
        )
    )


def divider() -> None:
    """
    Display a separator line.
    """

    console.rule(style="grey50")


# ==========================================================
# Progress
# ==========================================================

def progress(
    current: int,
    total: int,
    message: str,
) -> None:
    """
    Display progress information.
    """

    console.print(
        f"[bold cyan]"
        f"[{current}/{total}]"
        f"[/bold cyan] "
        f"{message}"
    )