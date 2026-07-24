"""
robots.txt Parser

Downloads and parses robots.txt.
"""

from urllib.parse import urljoin

from modules.crawler.helpers import download_page


# ==========================================================
# Download robots.txt
# ==========================================================

def download_robots(
    base_url: str,
) -> str | None:
    """
    Download robots.txt.
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
) -> dict:
    """
    Parse robots.txt.
    """

    result = {

        "allow": [],

        "disallow": [],

        "sitemaps": [],

        "user_agents": [],

        "crawl_delay": None,

        "host": None,

    }

    if not content:

        return result

    for line in content.splitlines():

        line = line.strip()

        if not line:

            continue

        if "#" in line:

            line = line.split(
                "#",
                1,
            )[0].strip()

        if not line:

            continue

        key, sep, value = line.partition(":")

        if not sep:

            continue

        key = key.lower().strip()

        value = value.strip()

        if not value:

            continue

        if key == "allow":

            result["allow"].append(
                value
            )

        elif key == "disallow":

            result["disallow"].append(
                value
            )

        elif key == "sitemap":

            result["sitemaps"].append(
                value
            )

        elif key == "user-agent":

            result["user_agents"].append(
                value
            )

        elif key == "crawl-delay":

            try:

                result["crawl_delay"] = float(
                    value
                )

            except ValueError:

                pass

        elif key == "host":

            result["host"] = value

    result["allow"] = sorted(
        set(result["allow"])
    )

    result["disallow"] = sorted(
        set(result["disallow"])
    )

    result["sitemaps"] = sorted(
        set(result["sitemaps"])
    )

    result["user_agents"] = sorted(
        set(result["user_agents"])
    )

    return result


# ==========================================================
# Fetch robots.txt
# ==========================================================

def fetch_robots(
    base_url: str,
) -> dict:
    """
    Download and parse robots.txt.
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

            "user_agents": [],

            "crawl_delay": None,

            "host": None,

        }

    result = parse_robots(
        content
    )

    result["robots"] = True

    return result