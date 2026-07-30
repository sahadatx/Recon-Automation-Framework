#!/usr/bin/env python3

"""
Framework Executor

Coordinates framework execution.
"""

from __future__ import annotations

from typing import Any

from core.analysis import empty_analysis
from core.context import ExecutionContext
from core.logger import warning
from core.plugins.manager import plugin_manager
from core.resolvers import resolve_inputs

Analysis = dict[str, Any]


def execute_module(
    context: ExecutionContext,
    module: str,
    *args: Any,
    **kwargs: Any,
) -> Analysis:
    """
    Execute one framework module.

    Workflow

        Resolve Inputs
              ↓
        Execute Plugin
              ↓
        Validate Result
              ↓
        Store Context
              ↓
        Return Analysis
    """

    if not args:

        args = resolve_inputs(
            module,
            context,
        )

    try:

        analysis = plugin_manager.execute(
            module,
            context,
            *args,
            **kwargs,
        )

    except Exception as exception:

        warning(
            f"{module}: {exception}"
        )

        analysis = empty_analysis()

    if not isinstance(
        analysis,
        dict,
    ):

        warning(
            f"{module} returned invalid analysis."
        )

        analysis = empty_analysis()

    context.set_analysis(
        module,
        analysis,
    )

    return analysis