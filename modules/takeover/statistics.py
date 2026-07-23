"""
Takeover Statistics

Generate statistics for
Subdomain Takeover
Detection.
"""

from __future__ import annotations

from collections import Counter


# ==========================================================
# Provider Statistics
# ==========================================================

def provider_statistics(
    results,
) -> dict:
    """
    Count takeover
    providers.

    Returns:
        dict
    """

    counter = Counter(

        result.get(

            "provider",

            "Unknown",

        )

        or "Unknown"

        for result

        in results

    )

    return dict(

        sorted(

            counter.items(),

        )

    )


# ==========================================================
# Confidence Statistics
# ==========================================================

def confidence_statistics(
    results,
) -> dict:
    """
    Count confidence
    levels.

    Returns:
        dict
    """

    return {

        "high": sum(

            result.get(

                "confidence",

                0,

            ) >= 90

            for result

            in results

        ),

        "medium": sum(

            70 <= result.get(

                "confidence",

                0,

            ) < 90

            for result

            in results

        ),

        "low": sum(

            0 < result.get(

                "confidence",

                0,

            ) < 70

            for result

            in results

        ),

        "unknown": sum(

            result.get(

                "confidence",

                0,

            ) == 0

            for result

            in results

        ),

    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results,
    elapsed=0.0,
) -> dict:
    """
    Generate takeover
    statistics.

    Returns:
        dict
    """

    total = len(

        results,

    )

    vulnerable = sum(

        result.get(

            "vulnerable",

            False,

        )

        for result

        in results

    )

    safe = (

        total

        - vulnerable

    )

    confidence = [

        result.get(

            "confidence",

            0,

        )

        for result

        in results

    ]

    average_confidence = round(

        sum(

            confidence,

        )

        / total,

        2,

    ) if total else 0.0

    highest_confidence = max(

        confidence,

        default=0,

    )

    statistics = (

        confidence_statistics(

            results,

        )

    )


    return {

        "targets": total,

        "vulnerable": vulnerable,

        "safe": safe,

        "provider_statistics": (

            provider_statistics(

                results,

            )

        ),

        "confidence_statistics": (

            statistics

        ),

        "average_confidence": (

            average_confidence

        ),

        "highest_confidence": (

            highest_confidence

        ),

        "elapsed": round(

            elapsed,

            2,

        ),

    }


# ==========================================================
# Print Summary
# ==========================================================

def print_summary(
    statistics,
) -> None:
    """
    Print takeover
    summary.
    """

    print()

    print("=" * 80)

    print(

        "Subdomain Takeover Summary".center(

            80,

        )

    )

    print("=" * 80)

    print(

        f"Targets               : {statistics['targets']}"

    )

    print(

        f"Vulnerable            : {statistics['vulnerable']}"

    )

    print(

        f"Safe                  : {statistics['safe']}"

    )

    print(

        f"Average Confidence    : "

        f"{statistics['average_confidence']}"

    )

    print(

        f"Highest Confidence    : "

        f"{statistics['highest_confidence']}"

    )

    print(

        f"Elapsed Time          : "

        f"{statistics['elapsed']} sec"

    )

    print("-" * 80)

    print(

        "Confidence Levels"

    )

    print("-" * 80)

    for level, count in statistics[
        "confidence_statistics"
    ].items():

        print(

            f"{level.title():<30}{count}"

        )

    print("-" * 80)

    print(

        "Takeover Providers"

    )

    print("-" * 80)

    providers = statistics.get(

        "provider_statistics",

        {},

    )

    if providers:

        for provider, count in providers.items():

            print(

                f"{provider:<30}{count}"

            )

    else:

        print(

            "None"

        )

    print("=" * 80)


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "provider_statistics",

    "confidence_statistics",

    "generate_statistics",

    "print_summary",

]