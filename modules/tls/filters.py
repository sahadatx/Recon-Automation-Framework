from __future__ import annotations

from copy import deepcopy


MAX_RISK_SCORE = 100

VALID_RISK_LEVELS = {
    "Safe",
    "Low",
    "Medium",
    "High",
    "Critical",
}


def reset_analysis(
    result: dict,
):


    result["risk_score"] = 0

    result["risk_level"] = "Safe"

    result["recommendations"] = []

    return result


def normalize_risk_score(
    score,
):


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


def normalize_recommendations(
    recommendations,
):


    if not recommendations:

        return []

    return sorted({item.strip() for item in recommendations if item and item.strip()})


def validate_risk_level(
    level,
):


    if level in VALID_RISK_LEVELS:

        return level

    return "Safe"


def validate_analysis(
    result,
):


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


def filter_result(
    result,
):


    filtered = deepcopy(
        result,
    )

    filtered = validate_analysis(
        filtered,
    )

    return filtered


def filter_results(
    results,
):


    filtered = [
        filter_result(
            result,
        )
        for result in results
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


def high_risk_only(
    results,
):


    return [
        result
        for result in results
        if result.get(
            "risk_level",
        )
        in {
            "High",
            "Critical",
        }
    ]


def safe_only(
    results,
):


    return [
        result
        for result in results
        if result.get(
            "risk_level",
        )
        == "Safe"
    ]


def failed_only(
    results,
):


    return [
        result
        for result in results
        if result.get(
            "error",
        )
    ]


def remove_failed(
    results,
):


    return [
        result
        for result in results
        if not result.get(
            "error",
        )
    ]


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
