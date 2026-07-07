"""
Technology Detection Engine

Core technology detection logic.
"""

from modules.tech.fingerprints import (
    SERVER_FINGERPRINTS,
    FRAMEWORK_FINGERPRINTS,
    CDN_FINGERPRINTS,
    CMS_FINGERPRINTS,
    HOSTING_FINGERPRINTS,
)

from modules.tech.helpers import (
    normalize_technologies,
    extract_headers,
    extract_html,
    detect_security_headers,
    detect_html_technologies,
)


# ==========================================================
# Detect Server
# ==========================================================

def detect_server(
    headers: dict,
) -> list[str]:
    """
    Detect web server technology.
    """

    technologies = []

    server = headers.get(
        "server",
        ""
    ).lower()

    for keyword, technology in SERVER_FINGERPRINTS.items():

        if keyword in server:

            technologies.append(
                technology
            )

    return normalize_technologies(
        technologies
    )


# ==========================================================
# Detect Powered-By
# ==========================================================

def detect_powered_by(
    headers: dict,
) -> list[str]:
    """
    Detect framework/runtime from headers.
    """

    technologies = []

    powered = headers.get(
        "x-powered-by",
        ""
    ).lower()

    for keyword, technology in FRAMEWORK_FINGERPRINTS.items():

        if keyword in powered:

            technologies.append(
                technology
            )

    return normalize_technologies(
        technologies
    )


# ==========================================================
# Detect CDN
# ==========================================================

def detect_cdn(
    headers: dict,
) -> list[str]:
    """
    Detect CDN/WAF technologies.
    """

    technologies = []

    for header, value in headers.items():

        text = (
            f"{header} {value}"
        ).lower()

        for keyword, technology in CDN_FINGERPRINTS.items():

            if keyword in text:

                technologies.append(
                    technology
                )

    return normalize_technologies(
        technologies
    )


# ==========================================================
# Detect CMS
# ==========================================================

def detect_cms(
    html: str,
) -> list[str]:
    """
    Detect CMS technologies.
    """

    technologies = []

    html = html.lower()

    for keyword, technology in CMS_FINGERPRINTS.items():

        if keyword.lower() in html:

            technologies.append(
                technology
            )

    return normalize_technologies(
        technologies
    )


# ==========================================================
# Detect Hosting
# ==========================================================

def detect_hosting(
    response: dict,
) -> list[str]:
    """
    Detect hosting platform.
    """

    technologies = []

    text = " ".join(

        [

            response.get(
                "url",
                ""
            ),

            str(
                response.get(
                    "server",
                    ""
                )
            ),

        ]

    ).lower()

    for keyword, technology in HOSTING_FINGERPRINTS.items():

        if keyword in text:

            technologies.append(
                technology
            )

    return normalize_technologies(
        technologies
    )


# ==========================================================
# Detect Technologies
# ==========================================================

def detect_technologies(
    response: dict,
) -> dict:
    """
    Detect all supported technologies.

    Returns:
        dict
    """

    headers = extract_headers(
        response
    )

    html = extract_html(
        response
    )

    technologies = []

    technologies.extend(
        detect_server(
            headers
        )
    )

    technologies.extend(
        detect_powered_by(
            headers
        )
    )

    technologies.extend(
        detect_cdn(
            headers
        )
    )

    technologies.extend(
        detect_cms(
            html
        )
    )

    technologies.extend(
        detect_html_technologies(
            html
        )
    )

    technologies.extend(
        detect_hosting(
            response
        )
    )

    security = detect_security_headers(
        headers
    )

    return {

        "technologies":
            normalize_technologies(
                technologies
            ),

        "security_headers":
            security,

    }