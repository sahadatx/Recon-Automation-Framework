from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all
from .manager import run


class TLSPlugin(BasePlugin):


    name = "tls"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Analyze TLS/SSL configurations, "
        "certificate validity, supported "
        "protocols, ciphers, and overall "
        "security posture."
    )

    depends_on = ("http",)

    config = {
        "certificate": True,
        "protocols": True,
        "ciphers": True,
        "risk_analysis": True,
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


plugin = TLSPlugin()


__all__ = [
    "TLSPlugin",
    "plugin",
]
