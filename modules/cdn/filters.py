from __future__ import annotations

from copy import deepcopy

from .constants import (
    CDN_PROVIDERS,
    HIGH_CONFIDENCE,
    LOW_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    UNKNOWN_CONFIDENCE,
)


VALID_PROVIDERS = set(CDN_PROVIDERS)

VALID_CONFIDENCE = {
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    LOW_CONFIDENCE,
    UNKNOWN_CONFIDENCE,
}


def reset_analysis(
    result: dict,
) -> dict:


    result["cdn"] = False

    result["provider"] = ""

    result["confidence"] = UNKNOWN_CONFIDENCE

    result["method"] = []

    result["recommendations"] = []

    return result


def normalize_confidence(
    confidence,
) -> int:


    try:

        confidence = int(
            confidence,
        )

    except Exception:

        confidence = UNKNOWN_CONFIDENCE

    confidence = max(
        0,
        min(
            confidence,
            100,
        ),
    )

    return confidence


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


def normalize_methods(
    methods,
) -> list[str]:


    if not methods:

        return []

    normalized = []

    for method in methods:

        if not method:

            continue

        method = (
            str(
                method,
            )
            .strip()
            .lower()
        )

        if method and method not in normalized:

            normalized.append(
                method,
            )

    return sorted(
        normalized,
    )


def normalize_recommendations(
    recommendations,
) -> list[str]:


    if not recommendations:

        return []

    return sorted({item.strip() for item in recommendations if item and item.strip()})


def validate_analysis(
    result,
) -> dict:


    result["confidence"] = normalize_confidence(
        result.get(
            "confidence",
            UNKNOWN_CONFIDENCE,
        )
    )

    result["provider"] = normalize_provider(
        result.get(
            "provider",
            "",
        )
    )

    result["method"] = normalize_methods(
        result.get(
            "method",
            [],
        )
    )

    result["recommendations"] = normalize_recommendations(
        result.get(
            "recommendations",
            [],
        )
    )

    result["cdn"] = bool(
        result.get(
            "provider",
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
                "confidence",
                UNKNOWN_CONFIDENCE,
            ),
            item.get(
                "provider",
                "",
            ),
        ),
        reverse=True,
    )

    return filtered


def detected_only(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if result.get(
            "cdn",
        )
    ]


def undetected_only(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if not result.get(
            "cdn",
        )
    ]


def failed_only(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if result.get(
            "error",
        )
    ]


def remove_failed(
    results,
) -> list[dict]:


    return [
        result
        for result in results
        if not result.get(
            "error",
        )
    ]


__all__ = [
    "VALID_PROVIDERS",
    "VALID_CONFIDENCE",
    "reset_analysis",
    "normalize_confidence",
    "normalize_provider",
    "normalize_methods",
    "normalize_recommendations",
    "validate_analysis",
    "filter_result",
    "filter_results",
    "detected_only",
    "undetected_only",
    "failed_only",
    "remove_failed",
]
