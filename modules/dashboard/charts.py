"""
Dashboard Charts

ASCII charts for the Dashboard module.
"""

from __future__ import annotations

# ==========================================================
# ASCII Bar
# ==========================================================


def ascii_bar(
    value: int,
    maximum: int,
    width: int = 40,
) -> str:
    """
    Generate an ASCII bar.

    Args:
        value:
            Current value.

        maximum:
            Maximum value.

        width:
            Maximum bar width.

    Returns:
        ASCII bar.
    """

    if maximum <= 0:
        return ""

    filled = int(value / maximum * width)

    return "█" * filled


# ==========================================================
# Build Chart
# ==========================================================


def build_chart(
    values: dict[str, int],
    width: int = 40,
) -> list[str]:
    """
    Build an ASCII chart.

    Args:
        values:
            Dashboard values.

        width:
            Maximum bar width.

    Returns:
        Chart lines.
    """

    if not values:
        return []

    maximum = max(
        values.values(),
        default=0,
    )

    lines: list[str] = []

    for label, value in values.items():

        bar = ascii_bar(
            value,
            maximum,
            width,
        )

        lines.append(f"{label:<20} {bar} {value}")

    return lines


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "ascii_bar",
    "build_chart",
]
