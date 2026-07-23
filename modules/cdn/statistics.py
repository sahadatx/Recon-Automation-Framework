"""
CDN Statistics

Generate statistics for
CDN Detection.
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
    Count CDN providers.

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
    Count confidence levels.

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
    Generate CDN statistics.

    Returns:
        dict
    """

    total = len(

        results,

    )

    detected = sum(

        result.get(

            "cdn",

            False,

        )

        for result

        in results

    )

    undetected = total - detected

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

    statistics = confidence_statistics(

        results,

    )

    return {

        "targets": total,

        "detected": detected,

        "undetected": undetected,

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
    Print CDN summary.
    """

    print()

    print("=" * 80)

    print(

        "CDN Detection Summary".center(

            80,

        )

    )

    print("=" * 80)

    print(

        f"Targets               : {statistics['targets']}"

    )

    print(

        f"CDN Detected          : {statistics['detected']}"

    )

    print(

        f"CDN Not Detected      : {statistics['undetected']}"

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

        "CDN Providers"

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