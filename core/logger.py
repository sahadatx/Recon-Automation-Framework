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

    console.rule(
        style="grey50"
    )


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


# ==========================================================
# Progress Bar
# ==========================================================

def progress_bar(
    current: int,
    total: int,
    width: int = 30,
) -> str:
    """
    Return a textual progress bar.

    Example:
    ████████████░░░░░░░░░░ 45%
    """

    if total <= 0:

        return ""

    ratio = current / total

    filled = int(
        width * ratio
    )

    empty = width - filled

    bar = (
        "█" * filled
        + "░" * empty
    )

    percent = ratio * 100

    return (
        f"{bar} "
        f"{percent:.0f}%"
    )


# ==========================================================
# Progress Line
# ==========================================================

def progress_status(
    current: int,
    total: int,
    message: str,
) -> None:
    """
    Display progress with a progress bar.

    Example:

    [123/207] ███████████░░░░░░░ 59%
    ✓ api.example.com (200 HTTPS)
    """

    bar = progress_bar(
        current,
        total,
    )

    console.print(
        f"[bold cyan]"
        f"[{current}/{total}]"
        f"[/bold cyan] "
        f"{bar} "
        f"{message}"
    )