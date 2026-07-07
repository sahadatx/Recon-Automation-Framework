"""
Sitemap Parser

Downloads and parses sitemap.xml files.
"""

from xml.etree import ElementTree
from urllib.parse import urljoin

from modules.crawler.helpers import (
    download_page,
)


# ==========================================================
# XML Namespace
# ==========================================================

SITEMAP_NS = {

    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",

}


# ==========================================================
# Download Sitemap
# ==========================================================

def download_sitemap(
    sitemap_url: str,
):
    """
    Download sitemap XML.

    Returns:
        str | None
    """

    response = download_page(
        sitemap_url
    )

    if response is None:

        return None

    return response.text


# ==========================================================
# Parse URL Sitemap
# ==========================================================

def parse_urlset(
    root,
):
    """
    Extract URLs from <urlset>.

    Returns:
        list[str]
    """

    urls = []

    for url in root.findall(
        "sm:url",
        SITEMAP_NS,
    ):

        loc = url.find(
            "sm:loc",
            SITEMAP_NS,
        )

        if (

            loc is not None

            and

            loc.text

        ):

            urls.append(
                loc.text.strip()
            )

    return urls


# ==========================================================
# Parse Sitemap Index
# ==========================================================

def parse_sitemap_index(
    root,
):
    """
    Extract sitemap URLs from
    <sitemapindex>.

    Returns:
        list[str]
    """

    sitemaps = []

    for sitemap in root.findall(
        "sm:sitemap",
        SITEMAP_NS,
    ):

        loc = sitemap.find(
            "sm:loc",
            SITEMAP_NS,
        )

        if (

            loc is not None

            and

            loc.text

        ):

            sitemaps.append(
                loc.text.strip()
            )

    return sitemaps


# ==========================================================
# Crawl Sitemap
# ==========================================================

def crawl_sitemap(
    sitemap_url: str,
    visited=None,
):
    """
    Download and recursively parse
    sitemap.xml.

    Returns:
        list[str]
    """

    if visited is None:

        visited = set()

    if sitemap_url in visited:

        return []

    visited.add(
        sitemap_url
    )

    content = download_sitemap(
        sitemap_url
    )

    if content is None:

        return []

    try:

        root = ElementTree.fromstring(
            content
        )

    except ElementTree.ParseError:

        return []

    tag = root.tag.lower()

    # ------------------------------------------
    # URLSET
    # ------------------------------------------

    if tag.endswith(
        "urlset"
    ):

        return parse_urlset(
            root
        )

    # ------------------------------------------
    # SITEMAP INDEX
    # ------------------------------------------

    if tag.endswith(
        "sitemapindex"
    ):

        urls = []

        sitemap_urls = parse_sitemap_index(
            root
        )

        for child in sitemap_urls:

            urls.extend(

                crawl_sitemap(
                    child,
                    visited,
                )

            )

        return urls

    return []


# ==========================================================
# Fetch Sitemap
# ==========================================================

def fetch_sitemap(
    base_url: str,
):
    """
    Download sitemap.xml.

    Returns:
        dict
    """

    sitemap_url = urljoin(

        base_url,

        "/sitemap.xml",

    )

    urls = crawl_sitemap(
        sitemap_url
    )

    urls = sorted(
        set(urls)
    )

    return {

        "sitemap": bool(
            urls
        ),

        "count": len(
            urls
        ),

        "urls": urls,

    }


# ==========================================================
# Fetch From robots.txt
# ==========================================================

def fetch_robot_sitemaps(
    sitemap_urls: list[str],
):
    """
    Parse sitemap URLs extracted
    from robots.txt.

    Returns:
        dict
    """

    discovered = []

    visited = set()

    for sitemap in sitemap_urls:

        discovered.extend(

            crawl_sitemap(

                sitemap,

                visited,

            )

        )

    discovered = sorted(
        set(discovered)
    )

    return {

        "sitemap": bool(
            discovered
        ),

        "count": len(
            discovered
        ),

        "urls": discovered,

    }
