from modules.tech.fingerprints import (
    CDN_FINGERPRINTS,
    CMS_FINGERPRINTS,
    FRAMEWORK_FINGERPRINTS,
    HOSTING_FINGERPRINTS,
    SERVER_FINGERPRINTS,
)
from modules.tech.helpers import (
    detect_html_technologies,
    detect_security_headers,
    extract_headers,
    extract_html,
    normalize_technologies,
)


def detect_server(
    headers: dict,
) -> list[str]:


    technologies = []

    server = headers.get("server", "").lower()

    for keyword, technology in SERVER_FINGERPRINTS.items():

        if keyword in server:

            technologies.append(technology)

    return normalize_technologies(technologies)


def detect_powered_by(
    headers: dict,
) -> list[str]:


    technologies = []

    powered = headers.get("x-powered-by", "").lower()

    for keyword, technology in FRAMEWORK_FINGERPRINTS.items():

        if keyword in powered:

            technologies.append(technology)

    return normalize_technologies(technologies)


def detect_cdn(
    headers: dict,
) -> list[str]:


    technologies = []

    for header, value in headers.items():

        text = (f"{header} {value}").lower()

        for keyword, technology in CDN_FINGERPRINTS.items():

            if keyword in text:

                technologies.append(technology)

    return normalize_technologies(technologies)


def detect_cms(
    html: str,
) -> list[str]:


    technologies = []

    html = html.lower()

    for keyword, technology in CMS_FINGERPRINTS.items():

        if keyword.lower() in html:

            technologies.append(technology)

    return normalize_technologies(technologies)


def detect_hosting(
    response: dict,
) -> list[str]:


    technologies = []

    text = " ".join(
        [
            response.get("url", ""),
            str(response.get("server", "")),
        ]
    ).lower()

    for keyword, technology in HOSTING_FINGERPRINTS.items():

        if keyword in text:

            technologies.append(technology)

    return normalize_technologies(technologies)


def detect_technologies(
    response: dict,
) -> dict:


    headers = extract_headers(response)

    html = extract_html(response)

    technologies = []

    technologies.extend(detect_server(headers))

    technologies.extend(detect_powered_by(headers))

    technologies.extend(detect_cdn(headers))

    technologies.extend(detect_cms(html))

    technologies.extend(detect_html_technologies(html))

    technologies.extend(detect_hosting(response))

    security = detect_security_headers(headers)

    return {
        "technologies": normalize_technologies(technologies),
        "security_headers": security,
    }
