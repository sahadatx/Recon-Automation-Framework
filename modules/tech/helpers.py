from modules.tech.fingerprints import HTML_KEYWORDS


def normalize_technologies(
    technologies: list[str],
) -> list[str]:


    return sorted(set(tech.strip() for tech in technologies if tech))


def extract_headers(
    response: dict,
) -> dict:


    headers = response.get("headers", {})

    return {str(key).lower(): str(value) for key, value in headers.items()}


def extract_html(
    response: dict,
) -> str:


    return response.get("html", "").lower()


def detect_security_headers(
    headers: dict,
) -> list[str]:


    security_headers = []

    checks = {
        "content-security-policy": "Content Security Policy",
        "strict-transport-security": "HSTS",
        "x-frame-options": "X-Frame-Options",
        "x-content-type-options": "X-Content-Type-Options",
        "referrer-policy": "Referrer Policy",
        "permissions-policy": "Permissions Policy",
    }

    for header, name in checks.items():

        if header in headers:

            security_headers.append(name)

    return security_headers


def detect_html_technologies(
    html: str,
) -> list[str]:


    technologies = []

    for technology, keywords in HTML_KEYWORDS.items():

        for keyword in keywords:

            if keyword.lower() in html:

                technologies.append(technology)

                break

    return normalize_technologies(technologies)
