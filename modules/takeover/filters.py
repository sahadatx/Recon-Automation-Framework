"""
Takeover Filters

Filter and normalize
Subdomain Takeover
analysis results.
"""

from __future__ import annotations

from copy import deepcopy

from .constants import (
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    LOW_CONFIDENCE,
    UNKNOWN_CONFIDENCE,
    TAKEOVER_PROVIDERS,
)


# ==========================================================
# Constants
# ==========================================================

VALID_PROVIDERS = set(

    TAKEOVER_PROVIDERS,

)

VALID_CONFIDENCE = {

    HIGH_CONFIDENCE,

    MEDIUM_CONFIDENCE,

    LOW_CONFIDENCE,

    UNKNOWN_CONFIDENCE,

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

    result["vulnerable"] = False

    result["provider"] = ""

    result["confidence"] = (

        UNKNOWN_CONFIDENCE

    )

    result["methods"] = []

    result["fingerprint"] = ""

    result["recommendations"] = []

    return result


# ==========================================================
# Normalize Confidence
# ==========================================================

def normalize_confidence(
    confidence,
) -> int:
    """
    Normalize confidence.

    Returns:
        int
    """

    try:

        confidence = int(

            confidence,

        )

    except Exception:

        confidence = (

            UNKNOWN_CONFIDENCE

        )

    confidence = max(

        0,

        min(

            confidence,

            100,

        ),

    )

    return confidence


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
# Normalize Methods
# ==========================================================

def normalize_methods(
    methods,
) -> list[str]:
    """
    Normalize detection
    methods.

    Returns:
        list[str]
    """

    if not methods:

        return []

    normalized: list[str] = []

    for method in methods:

        if not method:

            continue

        method = str(

            method,

        ).strip().lower()

        if (

            method

            and

            method not in normalized

        ):

            normalized.append(

                method,

            )

    return sorted(

        normalized,

    )


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

    result["confidence"] = (

        normalize_confidence(

            result.get(

                "confidence",

                UNKNOWN_CONFIDENCE,

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

    result["methods"] = (

        normalize_methods(

            result.get(

                "methods",

                [],

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

    result["vulnerable"] = bool(

        result.get(

            "provider",

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


# ==========================================================
# Vulnerable Only
# ==========================================================

def vulnerable_only(
    results,
) -> list[dict]:
    """
    Return vulnerable
    results.

    Returns:
        list[dict]
    """

    return [

        result

        for result

        in results

        if result.get(

            "vulnerable",

        )

    ]


# ==========================================================
# Safe Only
# ==========================================================

def safe_only(
    results,
) -> list[dict]:
    """
    Return safe
    results.

    Returns:
        list[dict]
    """

    return [

        result

        for result

        in results

        if not result.get(

            "vulnerable",

        )

    ]


# ==========================================================
# Failed Only
# ==========================================================

def failed_only(
    results,
) -> list[dict]:
    """
    Return failed scans.

    Returns:
        list[dict]
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
) -> list[dict]:
    """
    Remove failed scans.

    Returns:
        list[dict]
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

    "vulnerable_only",

    "safe_only",

    "failed_only",

    "remove_failed",

]


