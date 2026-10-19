from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class DNSPlugin(BasePlugin):


    name = "dns"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Perform DNS enumeration and " "collect DNS records for " "target domains."
    )

    depends_on = ("passive",)

    config = {
        "output": True,
        "threads": True,
        "resolver": "system",
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


plugin = DNSPlugin()


__all__ = [
    "DNSPlugin",
    "plugin",
]
