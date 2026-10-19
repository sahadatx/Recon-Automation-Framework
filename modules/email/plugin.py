from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class EmailSecurityPlugin(BasePlugin):


    name = "email"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Analyze email security "
        "configuration including SPF, "
        "DKIM, DMARC, DNSSEC, BIMI, "
        "MTA-STS and TLS-RPT."
    )

    depends_on = ("dns",)

    config = {
        "threads": False,
        "output": True,
        "cache": False,
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


plugin = EmailSecurityPlugin()


__all__ = [
    "EmailSecurityPlugin",
    "plugin",
]
