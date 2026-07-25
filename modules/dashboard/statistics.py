"""
Dashboard Statistics

Generate dashboard statistics.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Empty Statistics
# ==========================================================

def empty_statistics() -> dict[str, Any]:
    """
    Return empty dashboard statistics.
    """

    return {
        "target": "",
        "modules": 0,
        "completed_modules": 0,
        "failed_modules": 0,
        "findings": 0,
        "elapsed": 0.0,
    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    report: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate dashboard statistics.

    Args:
        report:
            Complete report data.

    Returns:
        Dashboard statistics.
    """

    if not report:
        return empty_statistics()

    modules = report.get(
        "modules",
        {},
    )

    passive = modules.get(
        "passive",
        {},
    )

    target = passive.get(
        "statistics",
        {},
    ).get(
        "target",
        "",
    )

    completed_modules = sum(
        1
        for module in modules.values()
        if isinstance(
            module,
            dict,
        )
        and module
    )

    failed_modules = sum(
        1
        for module in modules.values()
        if (
            isinstance(
                module,
                dict,
            )
            and module.get(
                "failed",
            )
        )
    )

    findings = 0

    elapsed = 0.0

    for module in modules.values():

        if not isinstance(
            module,
            dict,
        ):
            continue

        results = module.get(
            "results",
            [],
        )

        if isinstance(
            results,
            (
                list,
                tuple,
                set,
                dict,
            ),
        ):

            findings += len(
                results,
            )

        elif results:

            findings += 1

        elapsed += module.get(
            "statistics",
            {},
        ).get(
            "elapsed",
            0.0,
        )

    return {

        "target": target,

        "modules": len(
            modules,
        ),

        "completed_modules": completed_modules,

        "failed_modules": failed_modules,

        "findings": findings,

        "elapsed": round(
            elapsed,
            2,
        ),

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "empty_statistics",
    "generate_statistics",
]