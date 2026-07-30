#!/usr/bin/env python3

"""
Module Executor
"""

from __future__ import annotations

import inspect

from typing import Any

from core.analysis import empty_analysis
from core.context import ExecutionContext
from core.logger import warning
from core.registry import get_runner
from core.resolvers import resolve_inputs


Analysis = dict[str, Any]


# ==========================================================
# Resolve Arguments
# ==========================================================

def _resolve_args(
    context: ExecutionContext,
    module: str,
    args: tuple[Any, ...],
) -> tuple[Any, ...]:
    """
    Resolve module input arguments.

    Explicit arguments always take precedence over
    automatically resolved dependencies.
    """

    if args:

        return args

    return resolve_inputs(
        module,
        context,
    )


# ==========================================================
# Validate Analysis
# ==========================================================

def _validate_analysis(
    module: str,
    analysis: Any,
) -> Analysis:
    """
    Ensure every module returns a valid analysis.
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


# ==========================================================
# Execute Runner
# ==========================================================

def _execute_runner(
    context: ExecutionContext,
    runner: Any,
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> Any:
    """
    Execute a module runner.

    If the runner accepts an ExecutionContext,
    inject the shared context automatically.

    Supports both:

        run(context, ...)
        run(...)

    and keyword-only:

        run(*, context=...)
    """

    signature = inspect.signature(
        runner,
    )

    parameters = signature.parameters

    context_parameter = parameters.get(
        "context",
    )

    if context_parameter is None:

        return runner(
            *args,
            **kwargs,
        )

    if (
        context_parameter.kind
        is inspect.Parameter.KEYWORD_ONLY
    ):

        return runner(
            *args,
            context=context,
            **kwargs,
        )

    return runner(
        context,
        *args,
        **kwargs,
    )


# ==========================================================
# Execute Module
# ==========================================================

def execute_module(
    context: ExecutionContext,
    module: str,
    *args: Any,
    **kwargs: Any,
) -> Analysis:
    """
    Execute a framework module.

    Workflow

        Resolve Inputs
            ↓
        Execute Runner
            ↓
        Validate Analysis
            ↓
        Store Analysis
            ↓
        Return Analysis
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

        analysis = _execute_runner(
            context=context,
            runner=runner,
            args=resolved_args,
            kwargs=kwargs,
        )

    except Exception as exception:

        warning(
            f"{module} failed: {exception}"
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


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "execute_module",
]