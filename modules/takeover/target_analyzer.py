"""
Subdomain Takeover Target Analyzer

Core analysis logic for
Subdomain Takeover Detection.
"""

from __future__ import annotations

from typing import Any

from .constants import (
    CNAME_FINGERPRINTS,
    HIGH_CONFIDENCE,
    LOW_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    METHOD_CNAME,
    METHOD_DNS,
    METHOD_HTTP,
    METHOD_STATUS,
    STATUS_CODES,
    TAKEOVER_FINGERPRINTS,
)
from .helpers import contains_fingerprint, create_result, merge_methods, safe_lower

# ==========================================================
# HTTP Body Detection
# ==========================================================


def detect_http_provider(
    body: str,
) -> tuple[str | None, str | None, list[str]]:

    if not body:
        return None, None, []

    for provider, fingerprints in TAKEOVER_FINGERPRINTS.items():

        fingerprint = contains_fingerprint(
            body,
            fingerprints,
        )

        if fingerprint:

            return (
                provider,
                fingerprint,
                [METHOD_HTTP],
            )

    return None, None, []


# ==========================================================
# Status Detection
# ==========================================================


def detect_status(
    status_code: int,
) -> list[str]:

    if status_code in STATUS_CODES:
        return [METHOD_STATUS]

    return []


# ==========================================================
# CNAME Detection
# ==========================================================


def detect_cname_provider(
    cname: str | None,
) -> tuple[str | None, list[str]]:

    if not cname:
        return None, []

    cname = safe_lower(cname)

    for provider, fingerprints in CNAME_FINGERPRINTS.items():

        for fingerprint in fingerprints:

            if safe_lower(fingerprint) in cname:

                return (
                    provider,
                    [METHOD_CNAME],
                )

    return None, []


# ==========================================================
# DNS Detection
# ==========================================================


def detect_dns(
    ip: str | None,
) -> list[str]:

    if ip:
        return [METHOD_DNS]

    return []


# ==========================================================
# Confidence
# ==========================================================


def calculate_confidence(
    methods: list[str],
) -> int:

    count = len(set(methods))

    if count >= 3:
        return HIGH_CONFIDENCE

    if count == 2:
        return MEDIUM_CONFIDENCE

    if count == 1:
        return LOW_CONFIDENCE

    return 0


# ==========================================================
# Recommendations
# ==========================================================


def build_recommendations(
    vulnerable: bool,
) -> list[str]:

    if vulnerable:

        return [
            "Possible subdomain takeover detected.",
            "Verify the DNS configuration.",
            "Confirm the finding manually before reporting.",
        ]

    return [
        "No takeover fingerprints detected.",
        "Manual verification is recommended.",
    ]


# ==========================================================
# Analyze Target
# ==========================================================


def analyze_target(
    target: str,
    body: str,
    status_code: int,
    cname: str | None,
    ip: str | None,
    http_title: str,
) -> dict[str, Any]:

    result = create_result()

    result["target"] = target

    provider: str | None = None
    fingerprint: str | None = None
    methods: list[str] = []

    detected, matched, current = detect_http_provider(body)

    if detected:
        provider = detected
        fingerprint = matched
        methods = merge_methods(methods, current)

    detected, current = detect_cname_provider(cname)

    if detected:
        provider = provider or detected
        methods = merge_methods(methods, current)

    methods = merge_methods(
        methods,
        detect_status(status_code),
    )

    methods = merge_methods(
        methods,
        detect_dns(ip),
    )

    vulnerable = provider is not None and len(methods) >= 2

    result["vulnerable"] = vulnerable
    result["provider"] = provider
    result["confidence"] = calculate_confidence(methods)
    result["methods"] = methods
    result["status_code"] = status_code
    result["fingerprint"] = fingerprint or ""
    result["cname"] = cname or ""
    result["ip"] = ip or ""
    result["http_title"] = http_title
    result["recommendations"] = build_recommendations(vulnerable)

    return result


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "detect_http_provider",
    "detect_status",
    "detect_cname_provider",
    "detect_dns",
    "calculate_confidence",
    "build_recommendations",
    "analyze_target",
]
