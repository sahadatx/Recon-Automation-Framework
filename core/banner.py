"""
Banner Module

Displays the framework banner.
"""

from rich.console import Console
from rich.panel import Panel

from config.config import (
    APP_NAME,
    VERSION,
    AUTHOR,
)

console = Console()


# ==========================================================
# Show Banner
# ==========================================================

def show_banner():
    """
    Display the application banner.
    """

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

    console.print(
        Panel.fit(
            banner,
            title="[bold cyan]Recon Framework[/bold cyan]",
            border_style="bright_blue",
        )
    )

    console.print(
        f"[bold]Application :[/bold] {APP_NAME}"
    )

    console.print(
        f"[bold]Version     :[/bold] {VERSION}"
    )

    console.print(
        f"[bold]Author      :[/bold] {AUTHOR}"
    )

    console.rule(style="bright_blue")