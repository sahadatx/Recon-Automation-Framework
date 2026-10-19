from rich.console import Console
from rich.rule import Rule

console = Console()


def info(message: str) -> None:

    console.print(f"[bold cyan][INFO][/bold cyan] {message}")


def success(message: str) -> None:

    console.print(f"[bold green][SUCCESS][/bold green] {message}")


def warning(message: str) -> None:

    console.print(f"[bold yellow][WARNING][/bold yellow] {message}")


def error(message: str) -> None:

    console.print(f"[bold red][ERROR][/bold red] {message}")


def debug(message: str) -> None:

    console.print(f"[bold magenta][DEBUG][/bold magenta] {message}")


def section(title: str) -> None:


    console.print()

    console.print(
        Rule(
            title,
            style="bold bright_blue",
        )
    )


def subsection(title: str) -> None:


    console.print()

    console.print(
        Rule(
            title,
            style="cyan",
        )
    )


def divider() -> None:


    console.rule(style="grey50")


def progress(
    current: int,
    total: int,
    message: str,
) -> None:


    console.print(f"[bold cyan]" f"[{current}/{total}]" f"[/bold cyan] " f"{message}")


def progress_bar(
    current: int,
    total: int,
    width: int = 30,
) -> str:


    if total <= 0:

        return ""

    ratio = current / total

    filled = int(width * ratio)

    empty = width - filled

    bar = "█" * filled + "░" * empty

    percent = ratio * 100

    return f"{bar} " f"{percent:.0f}%"


def progress_status(
    current: int,
    total: int,
    message: str,
) -> None:


    bar = progress_bar(
        current,
        total,
    )

    console.print(
        f"[bold cyan]" f"[{current}/{total}]" f"[/bold cyan] " f"{bar} " f"{message}"
    )
