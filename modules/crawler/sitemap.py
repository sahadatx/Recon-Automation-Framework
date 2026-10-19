import gzip
from urllib.parse import urljoin
from xml.etree import ElementTree

from core.logger import debug
from modules.crawler.helpers import download_page


SITEMAP_NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
}


MAX_SITEMAP_DEPTH = 5

MAX_SITEMAPS = 100


def download_sitemap(
    sitemap_url: str,
) -> str | None:


    response = download_page(sitemap_url)

    if response is None:

        return None

    content = response.content

    if sitemap_url.endswith(".gz"):

        try:

            content = gzip.decompress(content)

        except OSError:

            debug(f"Invalid gzip sitemap: {sitemap_url}")

            return None

    return content.decode(
        "utf-8",
        errors="ignore",
    )


def parse_urlset(
    root: ElementTree.Element,
) -> list[str]:


    urls = []

    for element in root.iter():

        if not element.tag.endswith("url"):

            continue

        for child in element:

            if child.tag.endswith("loc") and child.text:

                url = child.text.strip()

                if url.startswith(
                    (
                        "http://",
                        "https://",
                    )
                ):

                    urls.append(url)

                break

    return list(dict.fromkeys(urls))


def parse_sitemap_index(
    root: ElementTree.Element,
) -> list[str]:


    sitemaps = []

    for element in root.iter():

        if not element.tag.endswith("sitemap"):

            continue

        for child in element:

            if child.tag.endswith("loc") and child.text:

                url = child.text.strip()

                if url.startswith(
                    (
                        "http://",
                        "https://",
                    )
                ):

                    sitemaps.append(url)

                break

    return list(dict.fromkeys(sitemaps))


def crawl_sitemap(
    sitemap_url: str,
    visited: set[str] | None = None,
    depth: int = 0,
) -> list[str]:


    if visited is None:

        visited = set()


    if depth > MAX_SITEMAP_DEPTH:

        debug(f"Maximum sitemap depth reached: {sitemap_url}")

        return []


    if len(visited) >= MAX_SITEMAPS:

        debug("Maximum sitemap limit reached.")

        return []


    if sitemap_url in visited:

        return []

    visited.add(sitemap_url)


    content = download_sitemap(sitemap_url)

    if content is None:

        return []


    try:

        root = ElementTree.fromstring(content)

    except ElementTree.ParseError:

        debug(f"Invalid sitemap XML: {sitemap_url}")

        return []

    tag = root.tag.lower()


    if tag.endswith("urlset"):

        return parse_urlset(root)


    if tag.endswith("sitemapindex"):

        urls = []

        sitemap_urls = parse_sitemap_index(root)

        for child in sitemap_urls:

            urls.extend(
                crawl_sitemap(
                    child,
                    visited,
                    depth + 1,
                )
            )

        return list(dict.fromkeys(urls))

    debug(f"Unknown sitemap format: {sitemap_url}")

    return []


DEFAULT_SITEMAPS = (
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap.xml.gz",
)


def fetch_sitemap(
    base_url: str,
) -> dict:


    urls = []

    for path in DEFAULT_SITEMAPS:

        sitemap_url = urljoin(
            base_url,
            path,
        )

        discovered = crawl_sitemap(
            sitemap_url,
        )

        if discovered:

            urls.extend(discovered)

            break

    urls = sorted(set(urls))

    return {
        "found": bool(urls),
        "count": len(urls),
        "urls": urls,
    }


__all__ = [
    "download_sitemap",
    "parse_urlset",
    "parse_sitemap_index",
    "crawl_sitemap",
    "fetch_sitemap",
]
