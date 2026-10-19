from __future__ import annotations

from copy import deepcopy

from .constants import CRITICAL_RISK, HIGH_RISK, LOW_RISK, MAIL_PROVIDERS, MEDIUM_RISK


VALID_PROVIDERS = set(
    MAIL_PROVIDERS,
)

VALID_RISK = {
    LOW_RISK,
    MEDIUM_RISK,
    HIGH_RISK,
    CRITICAL_RISK,
}


def reset_analysis(
    result: dict,
) -> dict:


    result["provider"] = ""

    result["score"] = 0

    result["risk"] = LOW_RISK

    result["recommendations"] = []

    return result


def normalize_score(
    score,
) -> int:


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


def normalize_provider(
    provider,
) -> str:


    if not provider:

        return ""

    provider = str(
        provider,
    ).strip()

    if provider in VALID_PROVIDERS:

        return provider

    return ""


def normalize_risk(
    risk,
) -> str:


    if not risk:

        return LOW_RISK

    risk = str(
        risk,
    ).strip()

    if risk in VALID_RISK:

        return risk

    return LOW_RISK


def normalize_recommendations(
    recommendations,
) -> list[str]:


    if not recommendations:

        return []

    return sorted({item.strip() for item in recommendations if (item and item.strip())})


def validate_analysis(
    result,
) -> dict:


    result["score"] = normalize_score(
        result.get(
            "score",
            0,
        )
    )

    result["provider"] = normalize_provider(
        result.get(
            "provider",
            "",
        )
    )

    result["risk"] = normalize_risk(
        result.get(
            "risk",
            LOW_RISK,
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
) -> dict:


    filtered = deepcopy(
        result,
    )

    return validate_analysis(
        filtered,
    )


def filter_results(
    results,
) -> list[dict]:


    filtered = [
        filter_result(
            result,
        )
        for result in results
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


def high_risk_only(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if result.get(
            "risk",
        )
        in (
            HIGH_RISK,
            CRITICAL_RISK,
        )
    ]


def critical_only(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if result.get(
            "risk",
        )
        == CRITICAL_RISK
    ]


def remove_low_risk(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if result.get(
            "risk",
        )
        != LOW_RISK
    ]


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
