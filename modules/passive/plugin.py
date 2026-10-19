from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class PassivePlugin(BasePlugin):


    name = "passive"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Collect subdomains from multiple "
        "passive intelligence sources and "
        "merge, normalize, and analyze the "
        "results."
    )

    depends_on = ()

    config = {
        "threads": True,
        "retry": True,
        "merge": True,
        "normalize": True,
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


plugin = PassivePlugin()


__all__ = [
    "PassivePlugin",
    "plugin",
]
