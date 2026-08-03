#!/usr/bin/env python3

"""
Plugin Loader

Discovers and registers
framework plugins.
"""

from __future__ import annotations

from .base import BasePlugin
from .discovery import discovery
from .registry import registry

# ==========================================================
# Plugin Loader
# ==========================================================


class PluginLoader:
    """
    Discovers and registers
    framework plugins.
    """

    def __init__(
        self,
    ) -> None:

        self._loaded = False

    # ======================================================
    # Registration
    # ======================================================

    def register(
        self,
        plugin: BasePlugin,
    ) -> None:
        """
        Register a single plugin.
        """

        registry.register(
            plugin,
        )

    def register_many(
        self,
        plugins: list[BasePlugin],
    ) -> None:
        """
        Register multiple plugins.
        """

        for plugin in plugins:

            self.register(
                plugin,
            )

    # ======================================================
    # Loading
    # ======================================================

    def load_plugins(
        self,
    ) -> None:
        """
        Discover and register all
        framework plugins.
        """

        if self._loaded:

            return

        plugins = discovery.discover()

        self.register_many(
            plugins,
        )

        self._loaded = True

    # ======================================================
    # Reload
    # ======================================================

    def reload(
        self,
    ) -> None:
        """
        Reload all plugins.
        """

        registry.clear()

        self._loaded = False

        self.load_plugins()

    # ======================================================
    # Status
    # ======================================================

    @property
    def loaded(
        self,
    ) -> bool:
        """
        Whether plugins have
        already been loaded.
        """

        return self._loaded

    @property
    def plugin_count(
        self,
    ) -> int:
        """
        Return the number of
        registered plugins.
        """

        return len(
            registry,
        )


# ==========================================================
# Global Loader
# ==========================================================

loader = PluginLoader()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PluginLoader",
    "loader",
]
