from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from core.context import ExecutionContext

from .base import BasePlugin
from .loader import loader
from .registry import registry


class PluginManager:


    def initialize(self) -> None:


        loader.load_plugins()

        for plugin in self:

            plugin.initialize()


    def get(
        self,
        name: str,
    ) -> BasePlugin:


        return registry.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:


        return registry.exists(name)

    def all(
        self,
    ) -> list[BasePlugin]:


        return registry.all()


    def execute(
        self,
        name: str,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:


        plugin = self.get(name)

        if not plugin.enabled:

            return {}

        performance = context.performance

        performance.start_module(
            plugin.name,
        )

        try:

            plugin.before_run(
                context,
            )

            result = plugin.run(
                context,
                *args,
                **kwargs,
            )

            plugin.after_run(
                context,
                result,
            )

            plugin.before_export(
                result,
            )

            plugin.after_export(
                result,
            )

            return result

        finally:

            performance.stop_module(
                plugin.name,
            )


    def shutdown(self) -> None:


        for plugin in self:

            plugin.shutdown()


    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)

    def __iter__(
        self,
    ) -> Iterator[BasePlugin]:

        return (plugin for plugin in registry if plugin.enabled)

    def __len__(
        self,
    ) -> int:

        return len(
            list(self),
        )


plugin_manager = PluginManager()


__all__ = [
    "PluginManager",
    "plugin_manager",
]
