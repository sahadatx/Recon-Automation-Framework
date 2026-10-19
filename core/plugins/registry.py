from __future__ import annotations

from collections.abc import Iterator

from .base import BasePlugin


class PluginRegistry:


    def __init__(
        self,
    ) -> None:

        self._plugins: dict[
            str,
            BasePlugin,
        ] = {}


    def register(
        self,
        plugin: BasePlugin,
    ) -> None:


        name = plugin.name.strip().lower()

        if not name:

            raise ValueError("Plugin name cannot be empty.")

        if name in self._plugins:

            raise ValueError(f"Plugin '{name}' is already registered.")

        self._plugins[name] = plugin

    def unregister(
        self,
        name: str,
    ) -> None:


        self._plugins.pop(
            name.strip().lower(),
            None,
        )


    def get(
        self,
        name: str,
    ) -> BasePlugin:


        plugin = self._plugins.get(
            name.strip().lower(),
        )

        if plugin is None:

            raise KeyError(f"Plugin '{name}' is not registered.")

        return plugin

    def exists(
        self,
        name: str,
    ) -> bool:


        return name.strip().lower() in self._plugins


    def all(
        self,
    ) -> list[BasePlugin]:


        return list(
            self._plugins.values(),
        )

    def names(
        self,
    ) -> list[str]:


        return sorted(
            self._plugins,
        )

    def clear(
        self,
    ) -> None:


        self._plugins.clear()


    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(
            name,
        )

    def __len__(
        self,
    ) -> int:

        return len(
            self._plugins,
        )

    def __iter__(
        self,
    ) -> Iterator[BasePlugin]:

        return iter(
            self._plugins.values(),
        )

    def __getitem__(
        self,
        name: str,
    ) -> BasePlugin:

        return self.get(
            name,
        )


registry = PluginRegistry()


__all__ = [
    "PluginRegistry",
    "registry",
]
