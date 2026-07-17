"""
WAF Detector

Detect WAF vendor using
fingerprint matching.
"""

from __future__ import annotations

from typing import Any

from modules.waf.fingerprints import (
    WAF_FINGERPRINTS,
    CONFIDENCE,
    CONFIDENCE_LEVELS,
)

from modules.waf.helpers import (
    match_keys,
    match_substrings,
    normalize_headers,
    normalize_cookies,
    safe_lower,
    unique_evidence,
)

# ==========================================================
# Confidence Level
# ==========================================================

def get_confidence_level(score: int) -> str:
    """
    Convert score into confidence level.
    """

    for minimum, level in CONFIDENCE_LEVELS:

        if score >= minimum:

            return level

    return "Unknown"


# ==========================================================
# Evidence Builder
# ==========================================================

def build_evidence(category: str, matches: list[str]) -> list[str]:
    """
    Build evidence entries.
    """

    return [

        f"{category}: {item}"

        for item in matches

    ]


# ==========================================================
# Apply Score
# ==========================================================

def apply_score(
    score: int,
    evidence: list[str],
    category: str,
    matches: list[str],
    weight: int,
) -> int:
    """
    Apply score for one category.
    """

    if not matches:

        return score

    score += weight

    evidence.extend(

        build_evidence(

            category,

            matches,

        )

    )

    return score


# ==========================================================
# Detect Single Target
# ==========================================================

def detect_waf(scan: dict[str, Any]) -> dict[str, Any]:
    """
    Detect WAF vendor.
    """

    headers = normalize_headers(

        scan.get(

            "headers",

            {},

        )

    )

    cookies = normalize_cookies(

        scan.get(

            "cookies",

            {},

        )

    )

    server = safe_lower(

        scan.get(

            "server",

            "",

        )

    )

    body = safe_lower(

        scan.get(

            "body",

            "",

        )

    )

    status = scan.get(

        "status",

    )

    best = {

        "vendor": None,

        "score": 0,

        "confidence": "Unknown",

        "evidence": [],

    }

    for vendor, fp in WAF_FINGERPRINTS.items():

        matched_headers = match_keys(

            headers,

            fp["headers"],

        )

        matched_cookies = match_keys(

            cookies,

            fp["cookies"],

        )

        matched_server = match_substrings(

            server,

            fp["server"],

        )

        matched_body = match_substrings(

            body,

            fp["body"],

        )

        detected = (

            bool(

                matched_headers

            )

            or bool(

                matched_cookies

            )

            or (

                matched_server

                and matched_body

            )

        )

        if not detected:

            continue

        score = 0

        evidence = []

        score = apply_score(

            score,

            evidence,

            "Header",

            matched_headers,

            CONFIDENCE["header"],

        )

        score = apply_score(

            score,

            evidence,

            "Cookie",

            matched_cookies,

            CONFIDENCE["cookie"],

        )

        score = apply_score(

            score,

            evidence,

            "Server",

            matched_server,

            CONFIDENCE["server"],

        )

        score = apply_score(

            score,

            evidence,

            "Body",

            matched_body,

            CONFIDENCE["body"],

        )

        if (

            status in fp["status"]

            and (

                matched_headers

                or matched_cookies

                or matched_server

            )

        ):

            score += CONFIDENCE["status"]

            evidence.append(

                f"Status: {status}"

            )

        evidence = unique_evidence(

            evidence

        )

        if score > best["score"]:

            best = {

                "vendor": vendor,

                "score": score,

                "confidence": get_confidence_level(

                    score

                ),

                "evidence": evidence,

            }

    return {

        "url": scan.get(

            "url",

            "",

        ),

        "vendor": best["vendor"],

        "score": best["score"],

        "confidence": best["confidence"],

        "evidence": best["evidence"],

        "detected": best["vendor"] is not None,

    }


# ==========================================================
# Detect Multiple Targets
# ==========================================================

def detect_all(
    scans: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Detect WAF for multiple targets.
    """

    return [

        detect_waf(

            scan

        )

        for scan in scans

    ]