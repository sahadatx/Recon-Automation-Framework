"""
Technology Detection Helper Functions

Shared helper functions used by the
Technology Detection module.
"""

from modules.tech.fingerprints import (
    HTML_KEYWORDS,
)


# ==========================================================
# Normalize Technologies
# ==========================================================

def normalize_technologies(
    technologies: list[str],
) -> list[str]:
    """
    Remove duplicates and sort technologies.
    """

    return sorted(
        set(
            tech.strip()
            for tech in technologies
            if tech
        )
    )


# ==========================================================
# Extract Headers
# ==========================================================

def extract_headers(
    response: dict,
) -> dict:
    """
    Extract HTTP headers from response.

    Returns:
        dict
    """

    headers = response.get(
        "headers",
        {}
    )

    return {

        str(key).lower(): str(value)

        for key, value in headers.items()

    }


# ==========================================================
# Extract HTML
# ==========================================================

def extract_html(
    response: dict,
) -> str:
    """
    Extract HTML body.

    Returns:
        str
    """

    return response.get(
        "html",
        ""
    ).lower()


# ==========================================================
# Detect Security Headers
# ==========================================================

def detect_security_headers(
    headers: dict,
) -> list[str]:
    """
    Detect enabled security headers.

    Returns:
        list[str]
    """

    security_headers = []

    checks = {

        "content-security-policy":
            "Content Security Policy",

        "strict-transport-security":
            "HSTS",

        "x-frame-options":
            "X-Frame-Options",

        "x-content-type-options":
            "X-Content-Type-Options",

        "referrer-policy":
            "Referrer Policy",

        "permissions-policy":
            "Permissions Policy",

    }

    for header, name in checks.items():

        if header in headers:

            security_headers.append(
                name
            )

    return security_headers


# ==========================================================
# Detect HTML Technologies
# ==========================================================

def detect_html_technologies(
    html: str,
) -> list[str]:
    """
    Detect technologies from HTML source.

    Returns:
        list[str]
    """

    technologies = []

    for technology, keywords in HTML_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in html:

                technologies.append(
                    technology
                )

                break

    return normalize_technologies(
        technologies
    )