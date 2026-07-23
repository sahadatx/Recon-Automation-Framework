"""
Email Security Filters

Filter and normalize
Email Security
analysis results.
"""

from __future__ import annotations

from copy import deepcopy

from .constants import (
    CRITICAL_RISK,
    HIGH_RISK,
    LOW_RISK,
    MAIL_PROVIDERS,
    MEDIUM_RISK,
)

# ==========================================================
# Constants
# ==========================================================

VALID_PROVIDERS = set(

    MAIL_PROVIDERS,

)

VALID_RISK = {

    LOW_RISK,

    MEDIUM_RISK,

    HIGH_RISK,

    CRITICAL_RISK,

}

# ==========================================================
# Reset Analysis
# ==========================================================

def reset_analysis(
    result: dict,
) -> dict:
    """
    Reset invalid analysis.

    Returns:
        dict
    """

    result["provider"] = ""

    result["score"] = 0

    result["risk"] = LOW_RISK

    result["recommendations"] = []

    return result


# ==========================================================
# Normalize Score
# ==========================================================

def normalize_score(
    score,
) -> int:
    """
    Normalize score.

    Returns:
        int
    """

    try:

        score = int(

            score,

        )

    except Exception:

        score = 0

    score = max(

        0,

        min(

            score,

            100,

        ),

    )

    return score


# ==========================================================
# Normalize Provider
# ==========================================================

def normalize_provider(
    provider,
) -> str:
    """
    Normalize provider.

    Returns:
        str
    """

    if not provider:

        return ""

    provider = str(

        provider,

    ).strip()

    if provider in VALID_PROVIDERS:

        return provider

    return ""


# ==========================================================
# Normalize Risk
# ==========================================================

def normalize_risk(
    risk,
) -> str:
    """
    Normalize risk.

    Returns:
        str
    """

    if not risk:

        return LOW_RISK

    risk = str(

        risk,

    ).strip()

    if risk in VALID_RISK:

        return risk

    return LOW_RISK


# ==========================================================
# Normalize Recommendations
# ==========================================================

def normalize_recommendations(
    recommendations,
) -> list[str]:
    """
    Normalize
    recommendations.

    Returns:
        list[str]
    """

    if not recommendations:

        return []

    return sorted(

        {

            item.strip()

            for item

            in recommendations

            if (

                item

                and

                item.strip()

            )

        }

    )


# ==========================================================
# Validate Analysis
# ==========================================================

def validate_analysis(
    result,
) -> dict:
    """
    Validate analysis result.

    Returns:
        dict
    """

    result["score"] = (

        normalize_score(

            result.get(

                "score",

                0,

            )

        )

    )

    result["provider"] = (

        normalize_provider(

            result.get(

                "provider",

                "",

            )

        )

    )

    result["risk"] = (

        normalize_risk(

            result.get(

                "risk",

                LOW_RISK,

            )

        )

    )

    result["recommendations"] = (

        normalize_recommendations(

            result.get(

                "recommendations",

                [],

            )

        )

    )

    return result


# ==========================================================
# Filter Single Result
# ==========================================================

def filter_result(
    result,
) -> dict:
    """
    Filter one analysis
    result.

    Returns:
        dict
    """

    filtered = deepcopy(

        result,

    )

    return validate_analysis(

        filtered,

    )


# ==========================================================
# Filter Results
# ==========================================================

def filter_results(
    results,
) -> list[dict]:
    """
    Filter all analysis
    results.

    Returns:
        list[dict]
    """

    filtered = [

        filter_result(

            result,

        )

        for result

        in results

    ]

    filtered.sort(

        key=lambda item: (

            item.get(

                "score",

                0,

            ),

            item.get(

                "provider",

                "",

            ),

        ),

        reverse=True,

    )

    return filtered


# ==========================================================
# High Risk Only
# ==========================================================

def high_risk_only(
    results,
) -> list[dict]:
    """
    Return high risk
    results.

    Returns:
        list[dict]
    """

    return [

        result

        for result

        in results

        if result.get(

            "risk",

        )

        in

        (

            HIGH_RISK,

            CRITICAL_RISK,

        )

    ]


# ==========================================================
# Critical Only
# ==========================================================

def critical_only(
    results,
) -> list[dict]:
    """
    Return critical
    results.

    Returns:
        list[dict]
    """

    return [

        result

        for result

        in results

        if result.get(

            "risk",

        )

        ==

        CRITICAL_RISK

    ]


# ==========================================================
# Remove Low Risk
# ==========================================================

def remove_low_risk(
    results,
) -> list[dict]:
    """
    Remove low risk
    results.

    Returns:
        list[dict]
    """

    return [

        result

        for result

        in results

        if result.get(

            "risk",

        )

        !=

        LOW_RISK

    ]


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "VALID_PROVIDERS",

    "VALID_RISK",

    "reset_analysis",

    "normalize_score",

    "normalize_provider",

    "normalize_risk",

    "normalize_recommendations",

    "validate_analysis",

    "filter_result",

    "filter_results",

    "high_risk_only",

    "critical_only",

    "remove_low_risk",

]