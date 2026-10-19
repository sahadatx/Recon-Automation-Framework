from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class CDNPlugin(BasePlugin):


    name = "cdn"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Detect Content Delivery Networks "
        "using HTTP, DNS, CNAME and IP "
        "fingerprints."
    )

    depends_on = ("http",)

    config = {
        "http": True,
        "threads": False,
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


plugin = CDNPlugin()


__all__ = [
    "CDNPlugin",
    "plugin",
]
