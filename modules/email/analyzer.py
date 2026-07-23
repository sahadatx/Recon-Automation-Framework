"""
Email Security Analyzer

Core analysis logic for
Email Security.
"""

from __future__ import annotations

from typing import Any

from .constants import (
    CRITICAL_RISK,
    HIGH_RISK,
    HIGH_SCORE,
    LOW_RISK,
    LOW_SCORE,
    MAIL_PROVIDERS,
    MEDIUM_RISK,
    MEDIUM_SCORE,
)

from .helpers import (
    safe_lower,
)


# ==========================================================
# Mail Provider
# ==========================================================

def detect_provider(
    mx_records: list[str],
) -> str:
    """
    Detect mail provider
    using MX records.

    Returns:
        str
    """

    for record in mx_records:

        record = safe_lower(

            record,

        )

        for provider, fingerprints in MAIL_PROVIDERS.items():

            for fingerprint in fingerprints:

                if safe_lower(

                    fingerprint,

                ) in record:

                    return provider

    return ""


# ==========================================================
# Risk Score
# ==========================================================

def calculate_score(
    result: dict[str, Any],
) -> int:
    """
    Calculate email
    security score.

    Returns:
        int
    """

    score = 0

    if not result["mx"]:

        score += 10

    if not result["spf"]:

        score += 20

    if not result["dkim"]:

        score += 20

    if not result["dmarc"]:

        score += 20

    if not result["mta_sts"]:

        score += 10

    if not result["tls_rpt"]:

        score += 10

    if not result["bimi"]:

        score += 5

    if not result["dnssec"]:

        score += 5

    return score


# ==========================================================
# Risk Level
# ==========================================================

def calculate_risk(
    score: int,
) -> str:
    """
    Calculate risk level.

    Returns:
        str
    """

    if score <= LOW_SCORE:

        return LOW_RISK

    if score <= MEDIUM_SCORE:

        return MEDIUM_RISK

    if score <= HIGH_SCORE:

        return HIGH_RISK

    return CRITICAL_RISK

# ==========================================================
# Recommendations
# ==========================================================

def build_recommendations(
    result: dict[str, Any],
) -> list[str]:
    """
    Build recommendations.

    Returns:
        list[str]
    """

    recommendations: list[str] = []

    if not result["spf"]:

        recommendations.append(

            "Configure an SPF record.",

        )

    if not result["dkim"]:

        recommendations.append(

            "Configure DKIM signing.",

        )

    if not result["dmarc"]:

        recommendations.append(

            "Configure a DMARC policy.",

        )

    if not result["mta_sts"]:

        recommendations.append(

            "Enable MTA-STS.",

        )

    if not result["tls_rpt"]:

        recommendations.append(

            "Enable SMTP TLS Reporting.",

        )

    if not result["bimi"]:

        recommendations.append(

            "Consider enabling BIMI.",

        )

    if not result["dnssec"]:

        recommendations.append(

            "Enable DNSSEC protection.",

        )

    if not recommendations:

        recommendations.append(

            "Email security configuration looks healthy.",

        )

    return recommendations


# ==========================================================
# Analyze
# ==========================================================

def analyze(
    result: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyze email
    security.

    Returns:
        dict
    """

    result["provider"] = detect_provider(

        result["mx"],

    )

    result["score"] = calculate_score(

        result,

    )

    result["risk"] = calculate_risk(

        result["score"],

    )

    result["recommendations"] = (

        build_recommendations(

            result,

        )

    )

    return result


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "detect_provider",

    "calculate_score",

    "calculate_risk",

    "build_recommendations",

    "analyze",

]


