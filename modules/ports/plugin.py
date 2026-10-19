from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class PortScannerPlugin(BasePlugin):


    name = "ports"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Scan common TCP ports on live "
        "hosts and identify available "
        "network services."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "tcp": True,
        "common_ports": True,
        "output": True,
    }

    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:


        return run(
            context,
            *args,
            **kwargs,
        )

    def after_export(
        self,
        result: dict[str, Any],
    ) -> None:


        export_all(
            result,
        )


plugin = PortScannerPlugin()


__all__ = [
    "PortScannerPlugin",
    "plugin",
]
