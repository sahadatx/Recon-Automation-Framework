"""
Logger Module

Provides colorful logging utilities for the framework.
"""

from rich.console import Console

console = Console()


def info(message: str) -> None:
    """
    Display an informational message.
    """
    console.print(f"[bold cyan][INFO][/bold cyan] {message}")


def success(message: str) -> None:
    """
    Display a success message.
    """
    console.print(f"[bold green][SUCCESS][/bold green] {message}")


def warning(message: str) -> None:
    """
    Display a warning message.
    """
    console.print(f"[bold yellow][WARNING][/bold yellow] {message}")


def error(message: str) -> None:
    """
    Display an error message.
    """
    console.print(f"[bold red][ERROR][/bold red] {message}")


def debug(message: str) -> None:
    """
    Display a debug message.
    """
    console.print(f"[bold magenta][DEBUG][/bold magenta] {message}")