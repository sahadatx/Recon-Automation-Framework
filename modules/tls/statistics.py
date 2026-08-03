"""
TLS Security Statistics

Generate summary statistics
for TLS Security.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

# ==========================================================
# Risk Level Statistics
# ==========================================================


def risk_level_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:
    """
    Count risk levels.
    """

    order = [
        "Critical",
        "High",
        "Medium",
        "Low",
        "Safe",
    ]

    counter = Counter(
        result.get(
            "risk_level",
            "Safe",
        )
        for result in results
    )

    return {level: counter[level] for level in order}


# ==========================================================
# Security Statistics
# ==========================================================


def security_statistics(
    results: list[dict[str, Any]],
) -> dict[str, int]:
    """
    Count security findings.
    """

    return {
        "expired": sum(
            result.get(
                "expired",
                False,
            )
            for result in results
        ),
        "self_signed": sum(
            result.get(
                "self_signed",
                False,
            )
            for result in results
        ),
        "hostname_mismatch": sum(
            not result.get(
                "hostname_match",
                True,
            )
            for result in results
        ),
        "weak_protocol": sum(
            result.get(
                "weak_protocol",
                False,
            )
            for result in results
        ),
        "weak_cipher": sum(
            result.get(
                "weak_cipher",
                False,
            )
            for result in results
        ),
        "wildcard": sum(
            result.get(
                "wildcard",
                False,
            )
            for result in results
        ),
        "forward_secrecy": sum(
            result.get(
                "forward_secrecy",
                False,
            )
            for result in results
        ),
    }


# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generate TLS statistics.
    """

    total = len(results)

    scores = [
        result.get(
            "risk_score",
            0,
        )
        for result in results
    ]

    security = security_statistics(
        results,
    )

    return {
        "targets": total,
        "risk_levels": risk_level_statistics(
            results,
        ),
        "average_risk": (
            round(
                sum(scores) / total,
                2,
            )
            if total
            else 0.0
        ),
        "highest_risk": max(
            scores,
            default=0,
        ),
        "expired": security["expired"],
        "self_signed": security["self_signed"],
        "hostname_mismatch": security["hostname_mismatch"],
        "weak_protocol": security["weak_protocol"],
        "weak_cipher": security["weak_cipher"],
        "wildcard": security["wildcard"],
        "forward_secrecy": security["forward_secrecy"],
    }


# ==========================================================
# Empty Statistics
# ==========================================================


def empty_statistics() -> dict[str, Any]:
    """
    Return empty statistics.
    """

    return {
        "targets": 0,
        "risk_levels": {},
        "average_risk": 0.0,
        "highest_risk": 0,
        "expired": 0,
        "self_signed": 0,
        "hostname_mismatch": 0,
        "weak_protocol": 0,
        "weak_cipher": 0,
        "wildcard": 0,
        "forward_secrecy": 0,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "risk_level_statistics",
    "security_statistics",
    "generate_statistics",
    "empty_statistics",
]
