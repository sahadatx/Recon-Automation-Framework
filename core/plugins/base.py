#!/usr/bin/env python3

"""
Plugin Base Class

Defines the common interface for all
Recon Automation Framework plugins.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from core.context import ExecutionContext


# ==========================================================
# Base Plugin
# ==========================================================


class BasePlugin(ABC):
    """
    Abstract base class for all framework plugins.

    Plugin Lifecycle

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

    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    name: ClassVar[str] = ""

    version: ClassVar[str] = "1.0.0"

    author: ClassVar[str] = ""

    description: ClassVar[str] = ""

    # ------------------------------------------------------
    # Configuration
    # ------------------------------------------------------

    enabled: ClassVar[bool] = True

    depends_on: ClassVar[tuple[str, ...]] = ()

    config: ClassVar[dict[str, Any]] = {}

    # ======================================================
    # Lifecycle Hooks
    # ======================================================

    def initialize(self) -> None:
        """
        Called once after the plugin
        is registered.
        """

        pass

    def before_run(
        self,
        context: ExecutionContext,
    ) -> None:
        """
        Called immediately before
        plugin execution.
        """

        pass

    @abstractmethod
    def run(
        self,
        context: ExecutionContext,
        *args: Any,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute the plugin.

        Returns:
            Analysis dictionary.
        """

        raise NotImplementedError

    def after_run(
        self,
        context: ExecutionContext,
        result: dict[str, Any],
    ) -> None:
        """
        Called immediately after
        plugin execution.
        """

        pass

    def before_export(
        self,
        result: dict[str, Any],
    ) -> None:
        """
        Called immediately before
        exporting analysis.
        """

        pass

    def after_export(
        self,
        result: dict[str, Any],
    ) -> None:
        """
        Called immediately after
        exporting analysis.
        """

        pass

    def shutdown(self) -> None:
        """
        Called once before the
        framework exits.
        """

        pass


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "BasePlugin",
]