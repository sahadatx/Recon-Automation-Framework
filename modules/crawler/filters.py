"""
Crawler Filters

Filtering and normalization utilities used by the
URL Discovery module.
"""

from urllib.parse import (
    urlparse,
    urlunparse,
)


# ==========================================================
# Remove Fragment
# ==========================================================

def remove_fragment(
    url: str,
):
    """
    Remove URL fragment.

    Example:
        https://site.com/page#about
            ->
        https://site.com/page
    """

    parsed = urlparse(
        url
    )

    parsed = parsed._replace(
        fragment=""
    )

    return urlunparse(
        parsed
    )


# ==========================================================
# Remove Trailing Slash
# ==========================================================

def remove_trailing_slash(
    url: str,
):
    """
    Remove trailing slash.

    Example:
        https://site.com/page/
            ->
        https://site.com/page
    """

    parsed = urlparse(
        url
    )

    path = parsed.path

    if (

        path != "/"

        and

        path.endswith("/")

    ):

        path = path[:-1]

    parsed = parsed._replace(
        path=path
    )

    return urlunparse(
        parsed
    )


# ==========================================================
# Normalize URL
# ==========================================================

def normalize_url(
    url: str,
):
    """
    Normalize URL.

    Steps:

        • Remove fragment
        • Remove trailing slash

    Returns:
        str
    """

    url = remove_fragment(
        url
    )

    url = remove_trailing_slash(
        url
    )

    return url


# ==========================================================
# Same Domain
# ==========================================================

def same_domain(
    root_url: str,
    url: str,
):
    """
    Check whether URL belongs
    to the same domain.

    Returns:
        bool
    """

    return (

        urlparse(
            root_url
        ).netloc

        ==

        urlparse(
            url
        ).netloc

    )


# ==========================================================
# Is HTTP URL
# ==========================================================

def is_http_url(
    url: str,
):
    """
    Check whether URL uses
    HTTP or HTTPS.

    Returns:
        bool
    """

    scheme = urlparse(
        url
    ).scheme.lower()

    return scheme in (

        "http",

        "https",

    )



# ==========================================================
# Ignored Extensions
# ==========================================================

IGNORED_EXTENSIONS = {

    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".svg",
    ".ico",
    ".bmp",
    ".webp",

    ".pdf",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",

    ".mp3",
    ".wav",
    ".ogg",

    ".mp4",
    ".avi",
    ".mov",
    ".mkv",

    ".woff",
    ".woff2",
    ".ttf",
    ".eot",

    ".css",

}


# ==========================================================
# Extension Filter
# ==========================================================

def extension_filter(
    url: str,
):
    """
    Skip unwanted file extensions.

    Returns:
        bool
    """

    path = urlparse(
        url
    ).path.lower()

    return not any(

        path.endswith(
            extension
        )

        for extension

        in

        IGNORED_EXTENSIONS

    )


# ==========================================================
# Robots Filter
# ==========================================================

def robots_filter(
    url: str,
    rules: list[str],
):
    """
    Check robots.txt disallow rules.

    Returns:
        bool
    """

    if not rules:

        return True

    path = urlparse(
        url
    ).path

    for rule in rules:

        if (

            rule

            and

            path.startswith(
                rule
            )

        ):

            return False

    return True


# ==========================================================
# Duplicate Filter
# ==========================================================

def duplicate_filter(
    url: str,
    visited: set,
):
    """
    Skip visited URLs.

    Returns:
        bool
    """

    return url not in visited


# ==========================================================
# Depth Filter
# ==========================================================

def depth_filter(
    depth: int,
    max_depth: int,
):
    """
    Check crawl depth.

    Returns:
        bool
    """

    return depth <= max_depth


# ==========================================================
# Should Enqueue
# ==========================================================

def should_enqueue(
    root_url: str,
    url: str,
    visited: set,
    robots_rules: list[str],
    depth: int,
    max_depth: int,
):
    """
    Decide whether URL should be
    added into crawl queue.

    Returns:
        bool
    """

    url = normalize_url(
        url
    )

    if not is_http_url(
        url,
    ):

        return False

    if not same_domain(
        root_url,
        url,
    ):

        return False

    if not extension_filter(
        url,
    ):

        return False

    if not robots_filter(
        url,
        robots_rules,
    ):

        return False

    if not duplicate_filter(
        url,
        visited,
    ):

        return False

    if not depth_filter(
        depth,
        max_depth,
    ):

        return False

    return True


# ==========================================================
# Should Crawl
# ==========================================================

def should_crawl(
    url: str,
    visited: set,
):
    """
    Check whether URL should
    be crawled.

    Returns:
        bool
    """

    url = normalize_url(
        url
    )

    if not is_http_url(
        url,
    ):

        return False

    if not duplicate_filter(
        url,
        visited,
    ):

        return False

    return True


# ==========================================================
# Normalize URL List
# ==========================================================

def normalize_urls(
    urls: list[str],
):
    """
    Normalize and deduplicate URLs.

    Returns:
        list[str]
    """

    normalized = {

        normalize_url(
            url
        )

        for url in urls

        if is_http_url(
            url
        )

    }

    return sorted(
        normalized
    )

