"""
WAF Helpers

Reusable helper functions
for the WAF Detection module.
"""

from __future__ import annotations


# ==========================================================
# Safe Lower
# ==========================================================

def safe_lower(value):
    """
    Convert value to lowercase string.

    Returns:
        str
    """

    if value is None:

        return ""

    return str(value).lower()


# ==========================================================
# Normalize Headers
# ==========================================================

def normalize_headers(headers):
    """
    Normalize response headers.

    Returns:
        set
    """

    if not headers:

        return set()

    return {

        safe_lower(key)

        for key

        in headers.keys()

    }


# ==========================================================
# Normalize Cookies
# ==========================================================

def normalize_cookies(cookies):
    """
    Normalize cookie names.

    Returns:
        set
    """

    if not cookies:

        return set()

    return {

        safe_lower(key)

        for key

        in cookies.keys()

    }


# ==========================================================
# Extract Server
# ==========================================================

def extract_server(headers):
    """
    Extract Server header.

    Returns:
        str
    """

    if not headers:

        return ""

    return safe_lower(

        headers.get(

            "server",

            "",

        )

    )


# ==========================================================
# Match Keys
# ==========================================================

def match_keys(
    values,
    fingerprints,
):
    """
    Match keys against fingerprints.

    Returns:
        list
    """

    matches = []

    for fingerprint in fingerprints:

        if safe_lower(

            fingerprint

        ) in values:

            matches.append(

                fingerprint

            )

    return matches


# ==========================================================
# Match Substrings
# ==========================================================

def match_substrings(
    text,
    fingerprints,
):
    """
    Match substrings.

    Returns:
        list
    """

    text = safe_lower(

        text

    )

    matches = []

    for fingerprint in fingerprints:

        if safe_lower(

            fingerprint

        ) in text:

            matches.append(

                fingerprint

            )

    return matches


# ==========================================================
# Has Header
# ==========================================================

def has_header(
    headers,
    header,
):
    """
    Check if header exists.

    Returns:
        bool
    """

    return safe_lower(

        header

    ) in headers


# ==========================================================
# Has Cookie
# ==========================================================

def has_cookie(
    cookies,
    cookie,
):
    """
    Check if cookie exists.

    Returns:
        bool
    """

    return safe_lower(

        cookie

    ) in cookies


# ==========================================================
# Remove Duplicate Evidence
# ==========================================================

def unique_evidence(
    evidence,
):
    """
    Remove duplicate evidence.

    Returns:
        list
    """

    return sorted(

        {

            item.strip()

            for item

            in evidence

            if item

        }

    )


# ==========================================================
# Cap Score
# ==========================================================

def cap_score(
    score,
    maximum=100,
):
    """
    Cap score.

    Returns:
        int
    """

    if score < 0:

        return 0

    if score > maximum:

        return maximum

    return score