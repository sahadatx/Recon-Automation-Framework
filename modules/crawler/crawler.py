"""
URL Discovery Engine

Core crawler for discovering URLs.
"""

import time

from modules.crawler.queue import (
    CrawlQueue,
)

from modules.crawler.helpers import (
    download_page,
)

from modules.crawler.parser import (
    parse_html,
)

from modules.crawler.filters import (
    should_enqueue,
)

from core.logger import (
    debug,
    info,
    warning,
)

from config.config import (
    CRAWLER_DEPTH,
    CRAWLER_MAX_URLS,
)


from modules.crawler.robots import (
    fetch_robots,
)

from modules.crawler.sitemap import (
    fetch_sitemap,
)

# ==========================================================
# Create Statistics
# ==========================================================

def create_statistics():
    """
    Initialize crawl statistics.

    Returns:
        dict
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
):
    """
    Create crawl result object.

    Returns:
        dict
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
    url: str,
):
    """
    Crawl a single URL.

    Args:
        url:
            Target URL.

    Returns:
        dict | None
    """

    debug(
        f"Crawling {url}"
    )

    try:

        response = download_page(
            url
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
                response.text
            ),

            "parsed": parsed,

        }

    except Exception as error:

        warning(
            f"{url}: {error}"
        )

        return None
    


# ==========================================================
# Crawl Host
# ==========================================================

def crawl_host(
    host: str,
    use_sitemap: bool = False,
):
    """
    Crawl one host using BFS.

    Args:
        host:
            Target host.

    Returns:
        dict
    """

    info(
        f"Starting crawl: {host}"
    )

    start_time = time.perf_counter()

    result = create_result(
        host
    )

    queue = CrawlQueue()

    # ----------------------------------------------------------
    # Seed URL
    # ----------------------------------------------------------

    queue.enqueue(
        host,
        depth=0,
        parent=None,
    )

    # ----------------------------------------------------------
    # robots.txt
    # ----------------------------------------------------------

    try:

        robots = fetch_robots(
            host
        )

        robots_rules = robots.get(
            "disallow",
            [],
        )

    except Exception:

        robots_rules = []

    # ----------------------------------------------------------
    # Sitemap Integration (Optional)
    # ----------------------------------------------------------

    if use_sitemap:

        try:

            sitemap = fetch_sitemap(
                host
            )

            for sitemap_url in sitemap.get(
                "urls",
                [],
            ):

                if not queue.visited(
                    sitemap_url
                ):

                    queue.enqueue(

                        sitemap_url,

                        depth=1,

                        parent=host,

                    )

            info(
                f"Sitemap URLs: {sitemap.get('count', 0)}"
            )

        except Exception as error:

            warning(
                f"Sitemap: {error}"
            )

    # ----------------------------------------------------------
    # BFS Crawl
    # ----------------------------------------------------------

    while not queue.empty():

        # -----------------------------------------
        # Maximum URL Limit
        # -----------------------------------------

        if (

            queue.visited_count()

            >=

            CRAWLER_MAX_URLS

        ):

            warning(
                "Maximum crawl limit reached."
            )

            break

        item = queue.dequeue()

        if item is None:

            break

        url = item["url"]

        depth = item["depth"]

        parent = item["parent"]

        # -----------------------------------------
        # Depth Control
        # -----------------------------------------

        if depth > CRAWLER_DEPTH:

            continue

        # -----------------------------------------
        # Duplicate Check
        # -----------------------------------------

        if queue.visited(
            url
        ):

            continue

        queue.mark_visited(
            url
        )

        debug(
            f"[Depth {depth}] {url}"
        )

        page = crawl_url(
            url
        )

        if page is None:

            stats = result["statistics"]

            stats["failed"] += 1

            stats["failed_urls"].append(
                url
            )

            continue

        result["pages"][url] = page

        parsed = page["parsed"]

        internal = parsed.get(
            "internal_links",
            []
        )

        external = parsed.get(
            "external_links",
            []
        )

        javascript = parsed.get(
            "javascript",
            []
        )

        css = parsed.get(
            "css",
            []
        )

        forms = parsed.get(
            "forms",
            []
        )

        emails = parsed.get(
            "emails",
            []
        )

        # -----------------------------------------
        # Update Statistics
        # -----------------------------------------

        stats = result["statistics"]

        stats["pages"] += 1

        stats["visited"] = queue.visited_count()

        stats["queued"] = queue.size()

        stats["internal_urls"] += len(
            internal
        )

        stats["external_urls"] += len(
            external
        )

        stats["unique_javascript"].update(
            javascript
        )

        stats["unique_css"].update(
            css
        )

        stats["javascript"] = len(
            stats["unique_javascript"]
        )

        stats["css"] = len(
            stats["unique_css"]
        )

        stats["forms"] += len(
            forms
        )

        stats["emails"] += len(
            emails
        )

        # -----------------------------------------
        # Queue Internal Links
        # -----------------------------------------

        for link in internal:

            if should_enqueue(

                root_url=host,

                url=link,

                visited=queue.visited_urls(),

                robots_rules=robots_rules,

                depth=depth + 1,

                max_depth=CRAWLER_DEPTH,

            ):

                queue.enqueue(

                    link,

                    depth=depth + 1,

                    parent=url,

                )


    # -----------------------------------------
    # Finalize Statistics
    # -----------------------------------------

    stats = result["statistics"]

    stats["visited"] = queue.visited_count()

    stats["queued"] = queue.size()

    stats["unique_javascript"] = sorted(
        stats["unique_javascript"]
    )

    stats["unique_css"] = sorted(
        stats["unique_css"]
    )

    result["statistics"]["elapsed"] = round(
        time.perf_counter() - start_time,
        2,
    )

    return result



# ==========================================================
# Crawl Multiple Hosts
# ==========================================================

def crawl(
    hosts: list[str],
):
    """
    Crawl multiple hosts.

    Args:
        hosts:
            List of target hosts.

    Returns:
        dict
    """

    info(
        "Starting URL Discovery Engine..."
    )

    start = time.perf_counter()

    results = {}

    total_pages = 0

    total_failed = 0

    total_internal = 0

    total_external = 0

    total_js = 0

    total_css = 0

    total_forms = 0

    total_emails = 0

    for host in hosts:

        # -----------------------------------------
        # Crawl Host
        # -----------------------------------------

        result = crawl_host(
            host
        )

        results[host] = result

        stats = result["statistics"]

        total_pages += stats["pages"]

        total_failed += stats["failed"]

        total_internal += stats["internal_urls"]

        total_external += stats["external_urls"]

        total_js += stats["javascript"]

        total_css += stats["css"]

        total_forms += stats["forms"]

        total_emails += stats["emails"]

    elapsed = round(

        time.perf_counter()

        - start,

        2,

    )

    summary = {

        "hosts": len(
            hosts
        ),

        "pages": total_pages,

        "failed": total_failed,

        "internal_urls": total_internal,

        "external_urls": total_external,

        "javascript": total_js,

        "css": total_css,

        "forms": total_forms,

        "emails": total_emails,

        "elapsed": elapsed,

    }

    info(
        "-" * 60
    )

    info(
        "URL Discovery Summary"
    )

    info(
        "-" * 60
    )

    info(
        f"Hosts          : {summary['hosts']}"
    )

    info(
        f"Pages          : {summary['pages']}"
    )

    info(
        f"Failed         : {summary['failed']}"
    )

    info(
        f"Internal URLs  : {summary['internal_urls']}"
    )

    info(
        f"External URLs  : {summary['external_urls']}"
    )

    info(
        f"JavaScript     : {summary['javascript']}"
    )

    info(
        f"CSS            : {summary['css']}"
    )

    info(
        f"Forms          : {summary['forms']}"
    )

    info(
        f"Emails         : {summary['emails']}"
    )

    info(
        f"Elapsed        : {summary['elapsed']} sec"
    )

    info(
        "-" * 60
    )

    return {

        "results": results,

        "summary": summary,

    }