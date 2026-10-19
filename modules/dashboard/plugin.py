from __future__ import annotations

from typing import Any

from core.context import ExecutionContext
from core.plugins.base import BasePlugin

from .manager import run


class DashboardPlugin(BasePlugin):


    name = "dashboard"

    version = "1.0.0"

    author = "Sahadat Hossain"

    description = "Generate a unified dashboard " "from the framework report."

    depends_on = ("report",)

    config = {
        "output": True,
        "charts": True,
        "summary": True,
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


plugin = DashboardPlugin()


__all__ = [
    "DashboardPlugin",
    "plugin",
]
