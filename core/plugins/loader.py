from __future__ import annotations

from .base import BasePlugin
from .discovery import discovery
from .registry import registry


class PluginLoader:


    def __init__(
        self,
    ) -> None:

        self._loaded = False


    def register(
        self,
        plugin: BasePlugin,
    ) -> None:


        registry.register(
            plugin,
        )

    def register_many(
        self,
        plugins: list[BasePlugin],
    ) -> None:


        for plugin in plugins:

            self.register(
                plugin,
            )


    def load_plugins(
        self,
    ) -> None:


        if self._loaded:

            return

        plugins = discovery.discover()

        self.register_many(
            plugins,
        )

        self._loaded = True


    def reload(
        self,
    ) -> None:


        registry.clear()

        self._loaded = False

        self.load_plugins()


    @property
    def loaded(
        self,
    ) -> bool:


        return self._loaded

    @property
    def plugin_count(
        self,
    ) -> int:


        return len(
            registry,
        )


loader = PluginLoader()


__all__ = [
    "PluginLoader",
    "loader",
]
