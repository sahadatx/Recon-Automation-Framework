from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .exporter import export_all, show_summary
from .manager import run


class VHostPlugin(BasePlugin):


    name = "vhost"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = (
        "Discover virtual hosts using "
        "FFUF-based enumeration and "
        "identify interesting responses."
    )

    depends_on = ("http",)

    config = {
        "threads": True,
        "ffuf": True,
        "filters": True,
        "interesting": True,
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

        show_summary(
            result,
        )


plugin = VHostPlugin()


__all__ = [
    "VHostPlugin",
    "plugin",
]
