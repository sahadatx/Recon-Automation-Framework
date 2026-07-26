#!/usr/bin/env python3

"""
Module Executor
"""

from __future__ import annotations

from typing import Any

from core.analysis import empty_analysis
from core.context import ExecutionContext
from core.logger import warning
from core.registry import get_runner
from core.resolvers import resolve_inputs


Analysis = dict[str, Any]


def _resolve_args(
    context: ExecutionContext,
    module: str,
    args: tuple[Any, ...],
) -> tuple[Any, ...]:
    """
    Resolve module arguments.
    """

    if len(args) != 0:
        return args

    return resolve_inputs(
        module,
        context,
    )


def _validate_analysis(
    module: str,
    analysis: Any,
) -> Analysis:
    """
    Validate module analysis.
    """

    if analysis is None:
        return empty_analysis()

    if not isinstance(
        analysis,
        dict,
    ):
        warning(
            f"{module} returned invalid analysis."
        )

        return empty_analysis()

    return analysis


def execute_module(
    context: ExecutionContext,
    module: str,
    *args: Any,
    **kwargs: Any,
) -> Analysis:
    """
    Execute a module and store its analysis.
    """

    runner = get_runner(
        module,
    )

    resolved_args = _resolve_args(
        context,
        module,
        args,
    )

    try:

        analysis = runner(
            *resolved_args,
            **kwargs,
        )

    except Exception as error:

        warning(
            f"{module} failed: {error}"
        )

        analysis = empty_analysis()

    analysis = _validate_analysis(
        module,
        analysis,
    )

    context.set_analysis(
        module,
        analysis,
    )

    return analysis