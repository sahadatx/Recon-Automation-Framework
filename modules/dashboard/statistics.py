from __future__ import annotations

from typing import Any


def empty_statistics() -> dict[str, Any]:


    return {
        "target": "",
        "modules": 0,
        "completed_modules": 0,
        "failed_modules": 0,
        "findings": 0,
    }


def generate_statistics(
    report: dict[str, Any],
) -> dict[str, Any]:


    if not report:
        return empty_statistics()


    report_modules = report.get(
        "modules",
        {},
    )

    modules = report_modules.get(
        "analysis",
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
        and bool(module)
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
                False,
            )
        )
    )

    findings = 0

    for module in modules.values():

        if not isinstance(
            module,
            dict,
        ):
            continue

        results = module.get(
            "results",
        )

        if isinstance(
            results,
            dict,
        ):

            findings += len(
                results,
            )

        elif isinstance(
            results,
            (
                list,
                tuple,
                set,
            ),
        ):

            findings += len(
                results,
            )

        elif results is not None:

            findings += 1

    return {
        "target": target,
        "modules": len(
            modules,
        ),
        "completed_modules": completed_modules,
        "failed_modules": failed_modules,
        "findings": findings,
    }


__all__ = [
    "empty_statistics",
    "generate_statistics",
]
