"""
URL Discovery Engine

Core crawler for discovering URLs.
"""

from __future__ import annotations

import time
from typing import Any
import requests

from config.config import CRAWLER_DEPTH, CRAWLER_MAX_URLS
from core.context import ExecutionContext
from core.logger import debug, info, warning
from modules.crawler.filters import should_enqueue
from modules.crawler.helpers import download_page
from modules.crawler.parser import parse_html
from modules.crawler.queue import CrawlQueue
from modules.crawler.robots import fetch_robots
from modules.crawler.sitemap import fetch_sitemap

# ==========================================================
# Create Statistics
# ==========================================================


def create_statistics() -> dict:
    """
    Initialize crawler statistics.
    """

    return {
        "pages": 0,
        "visited": 0,
        "queued": 0,
        "internal_urls": 0,
        "external_urls": 0,
        "javascript": 0,
        "css": 0,
        "forms": 0,
        "emails": 0,
        "failed": 0,
        "elapsed": 0.0,
        "unique_javascript": set(),
        "unique_css": set(),
        "failed_urls": [],
    }


# ==========================================================
# Create Result
# ==========================================================


def create_result(
    host: str,
) -> dict:
    """
    Create crawler result object.
    """

    return {
        "host": host,
        "pages": {},
        "statistics": create_statistics(),
    }


# ==========================================================
# Crawl URL
# ==========================================================


def crawl_url(
    session: requests.Session,
    url: str,
) -> dict[str, Any] | None:
    """
    Crawl a single URL.

    Args:
        url:
            Target URL.

    Returns:
        Parsed page information.
    """

    debug(f"Crawling {url}")

    try:

        response = download_page(
            session=session,
            url=url,
        )

        if response is None:

            return None

        parsed = parse_html(
            url,
            response.text,
        )

        return {
            "url": url,
            "status": response.status_code,
            "content_type": response.headers.get(
                "Content-Type",
                "",
            ),
            "content_length": len(
                response.text,
            ),
            "parsed": parsed,
        }

    except Exception as error:

        warning(f"{url}: {error}")

        return None


# ==========================================================
# Initialize Queue
# ==========================================================


def initialize_queue(
    host: str,
) -> CrawlQueue:
    """
    Create crawl queue with seed URL.
    """

    queue = CrawlQueue()

    queue.enqueue(
        host,
        depth=0,
        parent=None,
    )

    return queue


# ==========================================================
# Load Robots Rules
# ==========================================================


def load_robots(
    host: str,
) -> list[str]:
    """
    Load robots.txt rules.
    """

    try:

        robots = fetch_robots(
            host,
        )

        return robots.get(
            "disallow",
            [],
        )

    except Exception:

        return []


# ==========================================================
# Load Sitemap
# ==========================================================


def load_sitemap(
    queue: CrawlQueue,
    host: str,
) -> None:
    """
    Seed queue using sitemap URLs.
    """

    try:

        sitemap = fetch_sitemap(
            host,
        )

        for url in sitemap.get(
            "urls",
            [],
        ):

            queue.enqueue(
                url,
                depth=1,
                parent=host,
            )

        info(f"Sitemap URLs: " f"{sitemap.get('count', 0)}")

    except Exception as error:

        warning(f"Sitemap: {error}")


# ==========================================================
# Update Statistics
# ==========================================================


def update_statistics(
    result: dict,
    queue: CrawlQueue,
    parsed: dict,
) -> None:
    """
    Update crawler statistics.
    """

    statistics = result["statistics"]

    internal = parsed.get(
        "internal_links",
        [],
    )

    external = parsed.get(
        "external_links",
        [],
    )

    javascript = parsed.get(
        "javascript",
        [],
    )

    css = parsed.get(
        "css",
        [],
    )

    forms = parsed.get(
        "forms",
        [],
    )

    emails = parsed.get(
        "emails",
        [],
    )

    statistics["pages"] += 1

    statistics["visited"] = queue.visited_count()

    statistics["queued"] = queue.size()

    statistics["internal_urls"] += len(internal)

    statistics["external_urls"] += len(external)

    statistics["unique_javascript"].update(javascript)

    statistics["unique_css"].update(css)

    statistics["javascript"] = len(statistics["unique_javascript"])

    statistics["css"] = len(statistics["unique_css"])

    statistics["forms"] += len(forms)

    statistics["emails"] += len(emails)


# ==========================================================
# Enqueue Internal Links
# ==========================================================


def enqueue_links(
    queue: CrawlQueue,
    host: str,
    parent: str,
    depth: int,
    links: list[str],
    robots_rules: list[str],
) -> None:
    """
    Add internal links into the queue.
    """

    for url in links:

        if not should_enqueue(
            root_url=host,
            url=url,
            visited=queue.visited_urls(),
            robots_rules=robots_rules,
            depth=depth + 1,
            max_depth=CRAWLER_DEPTH,
        ):

            continue

        queue.enqueue(
            url,
            depth=depth + 1,
            parent=parent,
        )


# ==========================================================
# Finalize Statistics
# ==========================================================


def finalize_statistics(
    result: dict,
    queue: CrawlQueue,
    start_time: float,
) -> None:
    """
    Finalize crawler statistics.
    """

    statistics = result["statistics"]

    statistics["visited"] = queue.visited_count()

    statistics["queued"] = queue.size()

    statistics["unique_javascript"] = sorted(statistics["unique_javascript"])

    statistics["unique_css"] = sorted(statistics["unique_css"])

    statistics["elapsed"] = round(
        time.perf_counter() - start_time,
        2,
    )


# ==========================================================
# Crawl Host
# ==========================================================


def crawl_host(
    context: ExecutionContext,
    host: str,
    use_sitemap: bool = False,
) -> dict[str, Any]:
    """
    Crawl one host using Breadth-First Search.

    Args:
        host:
            Target host.

        use_sitemap:
            Seed the queue from sitemap.xml.

    Returns:
        Crawl result.
    """

    info(f"Starting crawl: {host}")

    session = context.get_http_session()

    if session is None:

        raise RuntimeError("HTTP session not initialized.")

    start_time = time.perf_counter()

    result = create_result(
        host,
    )

    queue = initialize_queue(
        host,
    )

    robots_rules = load_robots(
        host,
    )

    if use_sitemap:

        load_sitemap(
            queue,
            host,
        )

    while not queue.empty():

        # --------------------------------------------------
        # Maximum URL Limit
        # --------------------------------------------------

        if queue.visited_count() >= CRAWLER_MAX_URLS:

            warning("Maximum crawl limit reached.")

            break

        item = queue.dequeue()

        if item is None:

            break

        url = item["url"]

        depth = item["depth"]

        # --------------------------------------------------
        # Depth Control
        # --------------------------------------------------

        if depth > CRAWLER_DEPTH:

            continue

        # --------------------------------------------------
        # Duplicate Check
        # --------------------------------------------------

        if queue.visited(
            url,
        ):

            continue

        queue.mark_visited(
            url,
        )

        debug(f"[Depth {depth}] {url}")

        page = crawl_url(
            session=session,
            url=url,
        )

        if page is None:

            statistics = result["statistics"]

            statistics["failed"] += 1

            statistics["failed_urls"].append(url)

            statistics["visited"] = queue.visited_count()

            statistics["queued"] = queue.size()

            continue

        result["pages"][url] = page

        parsed = page["parsed"]

        update_statistics(
            result=result,
            queue=queue,
            parsed=parsed,
        )

        enqueue_links(
            queue=queue,
            host=host,
            parent=url,
            depth=depth,
            links=parsed.get(
                "internal_links",
                [],
            ),
            robots_rules=robots_rules,
        )

    finalize_statistics(
        result=result,
        queue=queue,
        start_time=start_time,
    )

    return result


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "crawl_host",
]
