"""
TLS Filters

Filter and normalize
TLS analysis results.
"""

from __future__ import annotations

from copy import deepcopy

# ==========================================================
# Constants
# ==========================================================

MAX_RISK_SCORE = 100

VALID_RISK_LEVELS = {

    "Safe",

    "Low",

    "Medium",

    "High",

    "Critical",

}


# ==========================================================
# Reset Analysis
# ==========================================================

def reset_analysis(
    result: dict,
):
    """
    Reset invalid analysis.

    Returns:
        dict
    """

    result["risk_score"] = 0

    result["risk_level"] = "Safe"

    result["recommendations"] = []

    return result


# ==========================================================
# Normalize Risk Score
# ==========================================================

def normalize_risk_score(
    score,
):
    """
    Normalize risk score.

    Returns:
        int
    """

    try:

        score = int(score)

    except Exception:

        score = 0

    return max(

        0,

        min(

            score,

            MAX_RISK_SCORE,

        ),

    )


# ==========================================================
# Normalize Recommendations
# ==========================================================

def normalize_recommendations(
    recommendations,
):
    """
    Normalize recommendations.

    Returns:
        list
    """

    if not recommendations:

        return []

    return sorted(

        {

            item.strip()

            for item

            in recommendations

            if item and item.strip()

        }

    )


# ==========================================================
# Validate Risk Level
# ==========================================================

def validate_risk_level(
    level,
):
    """
    Validate risk level.

    Returns:
        str
    """

    if level in VALID_RISK_LEVELS:

        return level

    return "Safe"


# ==========================================================
# Validate Analysis
# ==========================================================

def validate_analysis(
    result,
):
    """
    Validate analysis result.

    Returns:
        dict
    """

    result["risk_score"] = normalize_risk_score(

        result.get(

            "risk_score",

            0,

        )

    )

    result["risk_level"] = validate_risk_level(

        result.get(

            "risk_level",

            "Safe",

        )

    )

    result["recommendations"] = normalize_recommendations(

        result.get(

            "recommendations",

            [],

        )

    )

    return result

# ==========================================================
# Filter Single Result
# ==========================================================

def filter_result(
    result,
):
    """
    Filter one analysis result.

    Returns:
        dict
    """

    filtered = deepcopy(

        result,

    )

    filtered = validate_analysis(

        filtered,

    )

    return filtered


# ==========================================================
# Filter Results
# ==========================================================

def filter_results(
    results,
):
    """
    Filter all analysis results.

    Returns:
        list
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

                "risk_score",

                0,

            ),

            item.get(

                "risk_level",

                "Safe",

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
):
    """
    Return High/Critical
    risk results.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if result.get(

            "risk_level",

        )

        in {

            "High",

            "Critical",

        }

    ]


# ==========================================================
# Safe Only
# ==========================================================

def safe_only(
    results,
):
    """
    Return Safe results.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if result.get(

            "risk_level",

        )

        == "Safe"

    ]


# ==========================================================
# Failed Only
# ==========================================================

def failed_only(
    results,
):
    """
    Return failed scans.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if result.get(

            "error",

        )

    ]


# ==========================================================
# Remove Failed
# ==========================================================

def remove_failed(
    results,
):
    """
    Remove failed scans.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if not result.get(

            "error",

        )

    ]


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "MAX_RISK_SCORE",

    "VALID_RISK_LEVELS",

    "reset_analysis",

    "normalize_risk_score",

    "normalize_recommendations",

    "validate_risk_level",

    "validate_analysis",

    "filter_result",

    "filter_results",

    "high_risk_only",

    "safe_only",

    "failed_only",

    "remove_failed",

]


