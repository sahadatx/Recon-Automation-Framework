"""
Email Security Statistics

Generate statistics for
Email Security.
"""

from __future__ import annotations

from collections import Counter

from .constants import (
    CRITICAL_RISK,
    HIGH_RISK,
    LOW_RISK,
    MEDIUM_RISK,
)


# ==========================================================
# Provider Statistics
# ==========================================================

def provider_statistics(
    results,
) -> dict:
    """
    Count mail
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
# Risk Statistics
# ==========================================================

def risk_statistics(
    results,
) -> dict:
    """
    Count risk
    levels.

    Returns:
        dict
    """

    return {

        "low": sum(

            result.get(

                "risk",

            ) == LOW_RISK

            for result

            in results

        ),

        "medium": sum(

            result.get(

                "risk",

            ) == MEDIUM_RISK

            for result

            in results

        ),

        "high": sum(

            result.get(

                "risk",

            ) == HIGH_RISK

            for result

            in results

        ),

        "critical": sum(

            result.get(

                "risk",

            ) == CRITICAL_RISK

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
    Generate email
    statistics.

    Returns:
        dict
    """

    total = len(

        results,

    )

    scores = [

        result.get(

            "score",

            0,

        )

        for result

        in results

    ]

    statistics = (

        risk_statistics(

            results,

        )

    )



    average_score = round(

        sum(

            scores,

        )

        / total,

        2,

    ) if total else 0.0

    highest_score = max(

        scores,

        default=0,

    )

    spf_enabled = sum(

        result.get(

            "spf",

            False,

        )

        for result

        in results

    )

    dkim_enabled = sum(

        result.get(

            "dkim",

            False,

        )

        for result

        in results

    )

    dmarc_enabled = sum(

        result.get(

            "dmarc",

            False,

        )

        for result

        in results

    )

    return {

        "targets": total,

        "low": statistics[

            "low"

        ],

        "medium": statistics[

            "medium"

        ],

        "high": statistics[

            "high"

        ],

        "critical": statistics[

            "critical"

        ],

        "provider_statistics": (

            provider_statistics(

                results,

            )

        ),

        "risk_statistics": (

            statistics

        ),

        "spf_enabled": (

            spf_enabled

        ),

        "dkim_enabled": (

            dkim_enabled

        ),

        "dmarc_enabled": (

            dmarc_enabled

        ),

        "average_score": (

            average_score

        ),

        "highest_score": (

            highest_score

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
    Print email
    summary.
    """

    print()

    print("=" * 80)

    print(

        "Email Security Summary".center(

            80,

        )

    )

    print("=" * 80)

    print(

        f"Targets               : {statistics['targets']}"

    )

    print(

        f"Low Risk              : {statistics['low']}"

    )

    print(

        f"Medium Risk           : {statistics['medium']}"

    )

    print(

        f"High Risk             : {statistics['high']}"

    )

    print(

        f"Critical Risk         : {statistics['critical']}"

    )

    print(

        f"SPF Enabled           : {statistics['spf_enabled']}"

    )

    print(

        f"DKIM Enabled          : {statistics['dkim_enabled']}"

    )

    print(

        f"DMARC Enabled         : {statistics['dmarc_enabled']}"

    )

    print(

        f"Average Score         : "

        f"{statistics['average_score']}"

    )

    print(

        f"Highest Score         : "

        f"{statistics['highest_score']}"

    )

    print(

        f"Elapsed Time          : "

        f"{statistics['elapsed']} sec"

    )

    print("-" * 80)

    print(

        "Risk Levels"

    )

    print("-" * 80)

    for level, count in statistics[
        "risk_statistics"
    ].items():

        print(

            f"{level.title():<30}{count}"

        )

    print("-" * 80)

    print(

        "Mail Providers"

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

    "risk_statistics",

    "generate_statistics",

    "print_summary",

]