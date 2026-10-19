from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class TakeoverPlugin(BasePlugin):


    name = "takeover"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Detect potential subdomain "
        "takeover vulnerabilities using "
        "DNS, CNAME, HTTP fingerprint "
        "and provider-specific analysis."
    )

    depends_on = (
        "http",
        "dns",
    )

    config = {
        "threads": True,
        "http": True,
        "dns": True,
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


plugin = TakeoverPlugin()


__all__ = [
    "TakeoverPlugin",
    "plugin",
]
