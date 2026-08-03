"""
Performance Report

Generate comprehensive performance reports.
"""

from __future__ import annotations

from typing import Any

# ==========================================================
# Generate Performance Report
# ==========================================================


def generate_report(
    *,
    execution_time: float,
    memory: dict[str, Any],
    bottlenecks: list[dict[str, Any]],
    benchmark: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Generate a comprehensive performance report.
    """

    report = {
        "execution": {
            "time_seconds": round(
                execution_time,
                3,
            ),
        },
        "memory": memory,
        "bottlenecks": bottlenecks,
        "summary": {
            "status": ("Healthy" if not bottlenecks else "Attention Required"),
            "bottleneck_count": len(
                bottlenecks,
            ),
        },
    }

    if benchmark is not None:

        report["benchmark"] = benchmark

    return report


# ==========================================================
# Markdown Report
# ==========================================================


def generate_markdown(
    report: dict[str, Any],
) -> str:
    """
    Convert report to Markdown.
    """

    execution = report["execution"]

    memory = report["memory"]

    summary = report["summary"]

    lines = [
        "# Performance Report",
        "",
        "## Execution",
        "",
        (f"- Execution Time: " f"{execution['time_seconds']:.3f} sec"),
        "",
        "## Memory",
        "",
        (f"- Current: " f"{memory['memory']['current_mb']:.2f} MB"),
        (f"- Peak: " f"{memory['memory']['peak_mb']:.2f} MB"),
        (f"- Difference: " f"{memory['memory']['difference_mb']:.2f} MB"),
        "",
        "## Summary",
        "",
        (f"- Status: " f"{summary['status']}"),
        (f"- Bottlenecks: " f"{summary['bottleneck_count']}"),
        "",
        "## Bottlenecks",
    ]

    if report["bottlenecks"]:

        for item in report["bottlenecks"]:

            lines.extend(
                [
                    (f"- **{item['category']}** " f"({item['severity']})"),
                    (f"  - Value: " f"{item['value']}"),
                    (f"  - Recommendation: " f"{item['recommendation']}"),
                ]
            )

    else:

        lines.append("- None detected.")

    if "benchmark" in report:

        benchmark = report["benchmark"]

        lines.extend(
            [
                "",
                "## Benchmark",
                "",
                (f"- Runs: " f"{benchmark.get('runs', 0)}"),
                (
                    f"- Average Peak Memory: "
                    f"{benchmark.get('average_peak_mb', 0.0):.2f} MB"
                ),
                (
                    f"- Lowest Peak Memory: "
                    f"{benchmark.get('lowest_peak_mb', 0.0):.2f} MB"
                ),
                (
                    f"- Highest Peak Memory: "
                    f"{benchmark.get('highest_peak_mb', 0.0):.2f} MB"
                ),
            ]
        )

    return "\n".join(
        lines,
    )


# ==========================================================
# Text Report
# ==========================================================


def generate_text(
    report: dict[str, Any],
) -> str:
    """
    Generate a plain-text report.
    """

    lines = [
        "=" * 60,
        "PERFORMANCE REPORT",
        "=" * 60,
        "",
        ("Execution Time : " f"{report['execution']['time_seconds']:.3f} sec"),
        ("Memory Peak    : " f"{report['memory']['memory']['peak_mb']:.2f} MB"),
        ("Status         : " f"{report['summary']['status']}"),
        ("Bottlenecks    : " f"{report['summary']['bottleneck_count']}"),
    ]

    if report["bottlenecks"]:

        lines.extend(
            [
                "",
                "Detected Bottlenecks:",
            ]
        )

        for item in report["bottlenecks"]:

            lines.append((f"- {item['category']} " f"[{item['severity']}]"))

    else:

        lines.extend(
            [
                "",
                "No bottlenecks detected.",
            ]
        )

    return "\n".join(
        lines,
    )


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_report",
    "generate_markdown",
    "generate_text",
]
