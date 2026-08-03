"""
TLS Security Analyzer

Analyze TLS Security results.
"""

from __future__ import annotations

from typing import Any

from .statistics import (
    generate_statistics,
)

# ==========================================================
# Analyze One Host
# ==========================================================


def analyze_host(
    certificate: dict[str, Any],
    protocols: dict[str, Any],
    cipher: dict[str, Any],
) -> dict[str, Any]:
    """
    Analyze one TLS target.

    Returns:
        Per-host TLS analysis.
    """

    expired = certificate.get(
        "expired",
        False,
    )

    self_signed = certificate.get(
        "self_signed",
        False,
    )

    hostname_match = certificate.get(
        "hostname_match",
        True,
    )

    wildcard = certificate.get(
        "wildcard",
        False,
    )

    weak_protocol = protocols.get(
        "security",
        "",
    ) in (
        "Weak",
        "Insecure",
        "Critical",
    )

    weak_cipher = cipher.get(
        "weak",
        False,
    )

    forward_secrecy = cipher.get(
        "forward_secrecy",
        False,
    )

    risk_score = 0

    if expired:
        risk_score += 40

    if self_signed:
        risk_score += 20

    if not hostname_match:
        risk_score += 20

    if weak_protocol:
        risk_score += 10

    if weak_cipher:
        risk_score += 10

    if risk_score >= 70:

        risk_level = "Critical"

    elif risk_score >= 50:

        risk_level = "High"

    elif risk_score >= 30:

        risk_level = "Medium"

    elif risk_score >= 10:

        risk_level = "Low"

    else:

        risk_level = "Safe"

    return {
        "host": certificate.get(
            "host",
            "",
        ),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "expired": expired,
        "self_signed": self_signed,
        "hostname_match": hostname_match,
        "wildcard": wildcard,
        "weak_protocol": weak_protocol,
        "weak_cipher": weak_cipher,
        "forward_secrecy": forward_secrecy,
        "certificate": certificate,
        "protocols": protocols,
        "cipher": cipher,
    }


# ==========================================================
# Analyze Results
# ==========================================================


def analyze(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Analyze TLS Security results.

    Args:
        results:
            TLS analysis results.

    Returns:
        TLS Security analysis.
    """

    return {
        "results": results,
        "statistics": generate_statistics(
            results,
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "analyze_host",
    "analyze",
]
