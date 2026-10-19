from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class FuzzingPlugin(BasePlugin):


    name = "fuzzing"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform directory and file "
        "fuzzing to discover hidden "
        "paths and interesting content."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
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


plugin = FuzzingPlugin()


__all__ = [
    "FuzzingPlugin",
    "plugin",
]
