#!/usr/bin/env python3

"""
Plugin Registry

Stores and manages all registered
framework plugins.
"""

from __future__ import annotations

from collections.abc import Iterator

from .base import BasePlugin

# ==========================================================
# Plugin Registry
# ==========================================================


class PluginRegistry:
    """
    Registry for framework plugins.
    """

    def __init__(
        self,
    ) -> None:

        self._plugins: dict[
            str,
            BasePlugin,
        ] = {}

    # ======================================================
    # Registration
    # ======================================================

    def register(
        self,
        plugin: BasePlugin,
    ) -> None:
        """
        Register a plugin.
        """

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
        """
        Unregister a plugin.
        """

        self._plugins.pop(
            name.strip().lower(),
            None,
        )

    # ======================================================
    # Lookup
    # ======================================================

    def get(
        self,
        name: str,
    ) -> BasePlugin:
        """
        Return a registered plugin.
        """

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
        """
        Check whether a plugin exists.
        """

        return name.strip().lower() in self._plugins

    # ======================================================
    # Collection
    # ======================================================

    def all(
        self,
    ) -> list[BasePlugin]:
        """
        Return all registered plugins.
        """

        return list(
            self._plugins.values(),
        )

    def names(
        self,
    ) -> list[str]:
        """
        Return registered plugin names.
        """

        return sorted(
            self._plugins,
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all plugins.
        """

        self._plugins.clear()

    # ======================================================
    # Dunder Methods
    # ======================================================

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


# ==========================================================
# Global Registry
# ==========================================================

registry = PluginRegistry()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PluginRegistry",
    "registry",
]
