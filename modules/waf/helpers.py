from __future__ import annotations


def safe_lower(value):


    if value is None:

        return ""

    return str(value).lower()


def normalize_headers(headers):


    if not headers:

        return set()

    return {safe_lower(key) for key in headers.keys()}


def normalize_cookies(cookies):


    if not cookies:

        return set()

    return {safe_lower(key) for key in cookies.keys()}


def extract_server(headers):


    if not headers:

        return ""

    return safe_lower(
        headers.get(
            "server",
            "",
        )
    )


def match_keys(
    values,
    fingerprints,
):


    matches = []

    for fingerprint in fingerprints:

        if safe_lower(fingerprint) in values:

            matches.append(fingerprint)

    return matches


def match_substrings(
    text,
    fingerprints,
):


    text = safe_lower(text)

    matches = []

    for fingerprint in fingerprints:

        if safe_lower(fingerprint) in text:

            matches.append(fingerprint)

    return matches


def has_header(
    headers,
    header,
):


    return safe_lower(header) in headers


def has_cookie(
    cookies,
    cookie,
):


    return safe_lower(cookie) in cookies


def unique_evidence(
    evidence,
):


    return sorted({item.strip() for item in evidence if item})


def cap_score(
    score,
    maximum=100,
):


    if score < 0:

        return 0

    if score > maximum:

        return maximum

    return score
