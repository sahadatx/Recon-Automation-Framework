from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class TechnologyPlugin(BasePlugin):


    name = "tech"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Identify web technologies and "
        "security headers used by "
        "discovered web applications."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "headers": True,
        "fingerprints": True,
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


plugin = TechnologyPlugin()


__all__ = [
    "TechnologyPlugin",
    "plugin",
]
