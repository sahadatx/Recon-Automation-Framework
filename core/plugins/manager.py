#!/usr/bin/env python3

"""
Plugin Manager

Coordinates the complete lifecycle
of framework plugins.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from core.context import ExecutionContext

from .base import BasePlugin
from .loader import loader
from .registry import registry


# ==========================================================
# Plugin Manager
# ==========================================================


class PluginManager:
    """
    Coordinates the lifecycle of all plugins.

        initialize()
              ↓
        before_run()
              ↓
            run()
              ↓
        after_run()
              ↓
        before_export()
              ↓
        after_export()
              ↓
          shutdown()
    """

    # ======================================================
    # Initialization
    # ======================================================

    def initialize(self) -> None:
        """
        Discover, register and initialize plugins.
        """

        loader.load_plugins()

        for plugin in self:

            plugin.initialize()

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

        return registry.get(name)

    def exists(
        self,
        name: str,
    ) -> bool:
        """
        Check whether a plugin exists.
        """

        return registry.exists(name)

    def all(
        self,
    ) -> list[BasePlugin]:
        """
        Return all registered plugins.
        """

        return registry.all()

    # ======================================================
    # Execution
    # ======================================================

    def execute(
        self,
        name: str,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute a plugin lifecycle.
        """

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

    # ======================================================
    # Shutdown
    # ======================================================

    def shutdown(self) -> None:
        """
        Shutdown all initialized plugins.
        """

        for plugin in self:

            plugin.shutdown()

    # ======================================================
    # Dunder Methods
    # ======================================================

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.exists(name)

    def __iter__(
        self,
    ) -> Iterator[BasePlugin]:

        return (
            plugin
            for plugin in registry
            if plugin.enabled
        )

    def __len__(
        self,
    ) -> int:

        return len(
            list(self),
        )


# ==========================================================
# Global Manager
# ==========================================================

plugin_manager = PluginManager()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PluginManager",
    "plugin_manager",
]