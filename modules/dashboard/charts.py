from __future__ import annotations


def ascii_bar(
    value: int,
    maximum: int,
    width: int = 40,
) -> str:


    if maximum <= 0:
        return ""

    filled = int(value / maximum * width)

    return "█" * filled


def build_chart(
    values: dict[str, int],
    width: int = 40,
) -> list[str]:


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


__all__ = [
    "ascii_bar",
    "build_chart",
]
