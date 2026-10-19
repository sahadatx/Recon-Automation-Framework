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


def create_statistics() -> dict:


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


def create_result(
    host: str,
) -> dict:


    return {
        "host": host,
        "pages": {},
        "statistics": create_statistics(),
    }


def crawl_url(
    session: requests.Session,
    url: str,
) -> dict[str, Any] | None:


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


def initialize_queue(
    host: str,
) -> CrawlQueue:


    queue = CrawlQueue()

    queue.enqueue(
        host,
        depth=0,
        parent=None,
    )

    return queue


def load_robots(
    host: str,
) -> list[str]:


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


def load_sitemap(
    queue: CrawlQueue,
    host: str,
) -> None:


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


def update_statistics(
    result: dict,
    queue: CrawlQueue,
    parsed: dict,
) -> None:


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


def enqueue_links(
    queue: CrawlQueue,
    host: str,
    parent: str,
    depth: int,
    links: list[str],
    robots_rules: list[str],
) -> None:


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


def finalize_statistics(
    result: dict,
    queue: CrawlQueue,
    start_time: float,
) -> None:


    statistics = result["statistics"]

    statistics["visited"] = queue.visited_count()

    statistics["queued"] = queue.size()

    statistics["unique_javascript"] = sorted(statistics["unique_javascript"])

    statistics["unique_css"] = sorted(statistics["unique_css"])

    statistics["elapsed"] = round(
        time.perf_counter() - start_time,
        2,
    )


def crawl_host(
    context: ExecutionContext,
    host: str,
    use_sitemap: bool = False,
) -> dict[str, Any]:


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


        if queue.visited_count() >= CRAWLER_MAX_URLS:

            warning("Maximum crawl limit reached.")

            break

        item = queue.dequeue()

        if item is None:

            break

        url = item["url"]

        depth = item["depth"]


        if depth > CRAWLER_DEPTH:

            continue


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


__all__ = [
    "crawl_host",
]
