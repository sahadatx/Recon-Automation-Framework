"""
robots.txt Parser

Downloads and parses robots.txt.
"""

from urllib.parse import (
    urljoin,
)

from modules.crawler.helpers import (
    download_page,
)


# ==========================================================
# Download robots.txt
# ==========================================================

def download_robots(
    base_url: str,
):
    """
    Download robots.txt.

    Args:
        base_url:
            Target website.

    Returns:
        str | None
    """

    robots_url = urljoin(
        base_url,
        "/robots.txt",
    )

    response = download_page(
        robots_url
    )

    if response is None:

        return None

    return response.text


# ==========================================================
# Parse robots.txt
# ==========================================================

def parse_robots(
    content: str,
):
    """
    Parse robots.txt.

    Returns:
        dict
    """

    result = {

        "allow": [],

        "disallow": [],

        "sitemaps": [],

    }

    if not content:

        return result

    for line in content.splitlines():

        line = line.strip()

        if (

            not line

            or

            line.startswith("#")

        ):

            continue

        lower = line.lower()

        if lower.startswith(
            "allow:"
        ):

            value = line.split(
                ":",
                1,
            )[1].strip()

            if value:

                result[
                    "allow"
                ].append(
                    value
                )

        elif lower.startswith(
            "disallow:"
        ):

            value = line.split(
                ":",
                1,
            )[1].strip()

            result[
                "disallow"
            ].append(
                value
            )

        elif lower.startswith(
            "sitemap:"
        ):

            value = line.split(
                ":",
                1,
            )[1].strip()

            if value:

                result[
                    "sitemaps"
                ].append(
                    value
                )

    return result


# ==========================================================
# Fetch robots.txt
# ==========================================================

def fetch_robots(
    base_url: str,
):
    """
    Download and parse robots.txt.

    Returns:
        dict
    """

    content = download_robots(
        base_url
    )

    if content is None:

        return {

            "robots": False,

            "allow": [],

            "disallow": [],

            "sitemaps": [],

        }

    result = parse_robots(
        content
    )

    result[
        "robots"
    ] = True

    return result
