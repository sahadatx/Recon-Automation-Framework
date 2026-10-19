from __future__ import annotations

from typing import Any


def generate_report(
    analysis: dict[str, Any],
) -> dict[str, Any]:


    memory = analysis.get(
        "memory",
        {},
    )

    result = analysis.get(
        "analysis",
        {},
    )

    return {
        "memory": {
            "current_mb": memory.get(
                "current_mb",
                0.0,
            ),
            "peak_mb": memory.get(
                "peak_mb",
                0.0,
            ),
            "difference_mb": memory.get(
                "difference_mb",
                0.0,
            ),
        },
        "analysis": {
            "status": result.get(
                "status",
                "Unknown",
            ),
            "grade": result.get(
                "grade",
                "-",
            ),
            "recommendations": result.get(
                "recommendations",
                [],
            ),
        },
        "statistics": {
            "current_memory": memory.get(
                "current_mb",
                0.0,
            ),
            "peak_memory": memory.get(
                "peak_mb",
                0.0,
            ),
            "difference": memory.get(
                "difference_mb",
                0.0,
            ),
            "recommendation_count": len(
                result.get(
                    "recommendations",
                    [],
                )
            ),
        },
    }


def generate_markdown(
    report: dict[str, Any],
) -> str:


    memory = report["memory"]

    analysis = report["analysis"]

    lines = [
        "# Memory Report",
        "",
        f"- **Current Memory:** {memory['current_mb']:.2f} MB",
        f"- **Peak Memory:** {memory['peak_mb']:.2f} MB",
        f"- **Difference:** {memory['difference_mb']:.2f} MB",
        f"- **Status:** {analysis['status']}",
        f"- **Grade:** {analysis['grade']}",
        "",
        "## Recommendations",
    ]

    recommendations = analysis["recommendations"]

    if recommendations:

        for item in recommendations:

            lines.append(f"- {item}")

    else:

        lines.append("- No recommendations.")

    return "\n".join(
        lines,
    )


__all__ = [
    "generate_report",
    "generate_markdown",
]
