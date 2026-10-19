from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from config.config import AUTHOR, VERSION

console = Console()


def show_banner(
    target: str | None = None,
    module_count: int | None = None,
) -> None:


    banner = r"""

 ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝

        Automation Framework
    """

    console.print()

    heading = Text("RECON AUTOMATION FRAMEWORK", style="bold bright_cyan")
    tagline = Text("MODULAR ATTACK SURFACE DISCOVERY", style="bright_white")

    details = Table.grid(padding=(0, 2))
    details.add_column(style="bold bright_blue", justify="right")
    details.add_column(style="white")
    details.add_row("VERSION", VERSION)
    details.add_row("AUTHOR", AUTHOR)

    if target:
        details.add_row("TARGET", target)

    if module_count is not None:
        details.add_row("PIPELINE", f"{module_count} modules")

    content = Table.grid(padding=(0, 1))
    content.add_column()
    content.add_row(Align.center(Text(banner, style="bold bright_cyan")))
    content.add_row(Align.center(heading))
    content.add_row(Align.center(tagline))
    content.add_row("")
    content.add_row(Align.center(details))

    console.print()
    console.print(
        Panel(
            content,
            border_style="bright_blue",
            padding=(1, 3),
        )
    )
