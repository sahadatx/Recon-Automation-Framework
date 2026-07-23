"""
CDN Analyzer

Core analysis logic for
CDN Detection.
"""

from __future__ import annotations

from typing import Any

from ipaddress import (
    ip_address,
    ip_network,
)

from .constants import (
    HEADER_FINGERPRINTS,
    SERVER_FINGERPRINTS,
    CNAME_FINGERPRINTS,
    IP_PROVIDER_HINTS,
    HIGH_CONFIDENCE,
    MEDIUM_CONFIDENCE,
    LOW_CONFIDENCE,
    METHOD_HEADER,
    METHOD_SERVER,
    METHOD_CNAME,
    METHOD_IP,
)

from .helpers import (
    create_result,
    merge_methods,
    safe_lower,
)


# ==========================================================
# Header Detection
# ==========================================================

def detect_header_provider(
    headers: dict[str, Any],
) -> tuple[str | None, list[str]]:
    """
    Detect CDN provider
    using HTTP headers.

    Returns:
        tuple[str | None, list[str]]
    """

    if not headers:

        return None, []

    normalized_headers = {

        key.lower(): safe_lower(value)

        for key, value in headers.items()

    }

    for provider, fingerprints in HEADER_FINGERPRINTS.items():

        for fingerprint in fingerprints:

            fingerprint = fingerprint.lower()

            if fingerprint in normalized_headers:

                return (

                    provider,

                    [

                        METHOD_HEADER,

                    ],

                )

    return None, []


# ==========================================================
# Server Detection
# ==========================================================

def detect_server_provider(
    server: str,
) -> tuple[str | None, list[str]]:
    """
    Detect CDN provider
    using Server header.

    Returns:
        tuple[str | None, list[str]]
    """

    if not server:

        return None, []

    server = safe_lower(

        server,

    )

    for fingerprint, provider in SERVER_FINGERPRINTS.items():

        if safe_lower(

            fingerprint,

        ) in server:

            return (

                provider,

                [

                    METHOD_SERVER,

                ],

            )

    return None, []


# ==========================================================
# CNAME Detection
# ==========================================================

def detect_cname_provider(
    cname: str,
) -> tuple[str | None, list[str]]:
    """
    Detect CDN provider
    using CNAME.

    Returns:
        tuple[str | None, list[str]]
    """

    if not cname:

        return None, []

    cname = safe_lower(

        cname,

    )

    for fingerprint, provider in CNAME_FINGERPRINTS.items():

        if safe_lower(

            fingerprint,

        ) in cname:

            return (

                provider,

                [

                    METHOD_CNAME,

                ],

            )

    return None, []


# ==========================================================
# IP Detection
# ==========================================================

def detect_ip_provider(
    ip: str,
) -> tuple[str | None, list[str]]:
    """
    Detect CDN provider
    using IP address.
    """

    if not ip:

        return None, []

    ip = safe_lower(

        ip,

    )

    for provider, prefixes in IP_PROVIDER_HINTS.items():

        for prefix in prefixes:

            if ip.startswith(

                safe_lower(

                    prefix,

                )

            ):

                return (

                    provider,

                    [

                        METHOD_IP,

                    ],

                )

    return None, []


# ==========================================================
# Confidence
# ==========================================================

def calculate_confidence(
    methods: list[str],
) -> int:
    """
    Calculate detection
    confidence.

    Returns:
        int
    """

    count = len(

        set(methods)

    )

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
    provider: str | None,
) -> list[str]:
    """
    Build recommendations.

    Returns:
        list[str]
    """

    recommendations: list[str] = []

    if provider:

        recommendations.append(

            f"CDN detected: {provider}"

        )

        recommendations.append(

            "Review CDN configuration."

        )

        recommendations.append(

            "Verify origin server exposure."

        )

    else:

        recommendations.append(

            "No CDN detected."

        )

        recommendations.append(

            "Verify manually."

        )

    return recommendations


# ==========================================================
# Analyze
# ==========================================================

def analyze(
    target: str,
    headers: dict[str, Any],
    server: str,
    cname: str | None,
    ip: str | None,
) -> dict[str, Any]:
    """
    Analyze CDN.

    Returns:
        dict
    """

    result = create_result()

    result["target"] = target

    provider: str | None = None

    methods: list[str] = []

    detected, current = detect_header_provider(

        headers,

    )

    if detected:

        provider = detected

        methods = merge_methods(

            methods,

            current,

        )

    detected, current = detect_server_provider(

        server,

    )

    if detected:

        provider = provider or detected

        methods = merge_methods(

            methods,

            current,

        )

    detected, current = detect_cname_provider(

        cname,

    )

    if detected:

        provider = provider or detected

        methods = merge_methods(

            methods,

            current,

        )

    detected, current = detect_ip_provider(

        ip,

    )

    if detected:

        provider = provider or detected

        methods = merge_methods(

            methods,

            current,

        )

    result["cdn"] = provider is not None

    result["provider"] = provider

    result["confidence"] = calculate_confidence(

        methods,

    )

    result["method"] = methods

    result["headers"] = headers

    result["cname"] = cname

    result["ip"] = ip

    result["recommendations"] = (

        build_recommendations(

            provider,

        )

    )

    return result


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "detect_header_provider",

    "detect_server_provider",

    "detect_cname_provider",

    "detect_ip_provider",

    "calculate_confidence",

    "build_recommendations",

    "analyze",

]