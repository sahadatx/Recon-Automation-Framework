#!/usr/bin/env python3

"""
Plugin Discovery

Automatically discovers framework plugins.
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

from .base import BasePlugin


# ==========================================================
# Plugin Discovery
# ==========================================================


class PluginDiscovery:
    """
    Discover plugins from framework packages.

    Expected layout:

        modules/
            passive/
                plugin.py

        plugins/
            custom/
                plugin.py
    """

    def __init__(
        self,
    ) -> None:

        self._packages: tuple[str, ...] = (
            "modules",
            "plugins",
        )

    # ======================================================
    # Discovery
    # ======================================================

    def discover(
        self,
    ) -> list[BasePlugin]:
        """
        Discover all enabled plugins.
        """

        discovered: dict[
            str,
            BasePlugin,
        ] = {}

        for package in self._packages:

            for plugin in self._discover_package(
                package,
            ):

                discovered.setdefault(
                    plugin.name.lower(),
                    plugin,
                )

        return sorted(
            discovered.values(),
            key=lambda plugin: plugin.name,
        )

    # ======================================================
    # Package Discovery
    # ======================================================

    def _discover_package(
        self,
        package: str,
    ) -> list[BasePlugin]:
        """
        Discover plugins from one package.
        """

        plugins: list[
            BasePlugin
        ] = []

        root = Path(package)

        if not root.is_dir():

            return plugins

        for directory in sorted(
            root.iterdir(),
            key=lambda item: item.name,
        ):

            if not directory.is_dir():

                continue

            if directory.name.startswith("."):

                continue

            module_name = (
                f"{package}."
                f"{directory.name}.plugin"
            )

            try:

                module = import_module(
                    module_name,
                )

            except ModuleNotFoundError:

                continue

            except Exception:

                continue

            plugin = getattr(
                module,
                "plugin",
                None,
            )

            if not isinstance(
                plugin,
                BasePlugin,
            ):

                continue

            if not plugin.enabled:

                continue

            plugins.append(
                plugin,
            )

        return plugins


# ==========================================================
# Global Discovery
# ==========================================================

discovery = PluginDiscovery()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PluginDiscovery",
    "discovery",
]