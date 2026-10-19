from __future__ import annotations

from typing import Any


TIME_WARNING = 5.0
TIME_CRITICAL = 15.0

MEMORY_WARNING = 250.0
MEMORY_CRITICAL = 500.0

CPU_WARNING = 70.0
CPU_CRITICAL = 90.0


def detect_bottlenecks(
    metrics: dict[str, Any],
) -> list[dict[str, Any]]:


    bottlenecks: list[dict[str, Any]] = []

    execution = metrics.get(
        "execution_time",
        0.0,
    )

    memory = metrics.get(
        "memory_peak_mb",
        0.0,
    )

    cpu = metrics.get(
        "cpu_percent",
        0.0,
    )


    if execution >= TIME_CRITICAL:

        bottlenecks.append(
            {
                "category": "Execution Time",
                "severity": "Critical",
                "value": execution,
                "recommendation": (
                    "Optimize slow modules or " "increase parallel execution."
                ),
            }
        )

    elif execution >= TIME_WARNING:

        bottlenecks.append(
            {
                "category": "Execution Time",
                "severity": "Warning",
                "value": execution,
                "recommendation": ("Review slow-running tasks."),
            }
        )


    if memory >= MEMORY_CRITICAL:

        bottlenecks.append(
            {
                "category": "Memory",
                "severity": "Critical",
                "value": memory,
                "recommendation": (
                    "Reduce memory usage or " "process data in batches."
                ),
            }
        )

    elif memory >= MEMORY_WARNING:

        bottlenecks.append(
            {
                "category": "Memory",
                "severity": "Warning",
                "value": memory,
                "recommendation": ("Review large objects and " "unused allocations."),
            }
        )


    if cpu >= CPU_CRITICAL:

        bottlenecks.append(
            {
                "category": "CPU",
                "severity": "Critical",
                "value": cpu,
                "recommendation": (
                    "Reduce CPU-intensive tasks " "or optimize algorithms."
                ),
            }
        )

    elif cpu >= CPU_WARNING:

        bottlenecks.append(
            {
                "category": "CPU",
                "severity": "Warning",
                "value": cpu,
                "recommendation": ("Investigate CPU-heavy modules."),
            }
        )

    return bottlenecks


def summary(
    bottlenecks: list[dict[str, Any]],
) -> str:


    if not bottlenecks:

        return "No performance bottlenecks detected."

    lines = [
        "Performance Bottlenecks",
        "-" * 30,
    ]

    for item in bottlenecks:

        lines.append(
            (
                f"[{item['severity']}] "
                f"{item['category']}: "
                f"{item['value']} "
                f"-> {item['recommendation']}"
            )
        )

    return "\n".join(
        lines,
    )


__all__ = [
    "detect_bottlenecks",
    "summary",
]
