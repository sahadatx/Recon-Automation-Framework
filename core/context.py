#!/usr/bin/env python3

"""
Execution Context
"""

from __future__ import annotations

from typing import Any


Analysis = dict[str, Any]


class ExecutionContext:
    """
    Stores analysis produced by each module.
    """

    def __init__(self) -> None:
        self._analysis: dict[str, Analysis] = {}

    def set_analysis(
        self,
        module: str,
        analysis: Analysis,
    ) -> None:
        """
        Store analysis for a module.
        """

        self._analysis[module] = analysis

    def get_analysis(
        self,
        module: str,
    ) -> Analysis:
        """
        Return analysis for a module.
        """

        return self._analysis.get(
            module,
            {},
        )

    def has_analysis(
        self,
        module: str,
    ) -> bool:
        """
        Check whether analysis exists.
        """

        return module in self._analysis

    def clear(self) -> None:
        """
        Remove all stored analysis.
        """

        self._analysis.clear()

    def to_dict(self) -> dict[str, Analysis]:
        """
        Return all analysis.
        """

        return dict(self._analysis)