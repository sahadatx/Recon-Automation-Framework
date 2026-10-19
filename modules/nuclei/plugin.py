from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class NucleiPlugin(BasePlugin):


    name = "nuclei"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform vulnerability scanning "
        "using Nuclei templates and "
        "generate consolidated findings."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "templates": "default",
        "output": True,
        "cleanup": True,
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


plugin = NucleiPlugin()


__all__ = [
    "NucleiPlugin",
    "plugin",
]
