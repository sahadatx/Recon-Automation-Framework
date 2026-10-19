from urllib.parse import urlparse, urlunparse


def remove_fragment(
    url: str,
):


    parsed = urlparse(url)

    parsed = parsed._replace(fragment="")

    return urlunparse(parsed)


def remove_trailing_slash(
    url: str,
):


    parsed = urlparse(url)

    path = parsed.path

    if path != "/" and path.endswith("/"):

        path = path[:-1]

    parsed = parsed._replace(path=path)

    return urlunparse(parsed)


def normalize_url(
    url: str,
):


    url = remove_fragment(url)

    url = remove_trailing_slash(url)

    return url


def same_domain(
    root_url: str,
    url: str,
):


    return urlparse(root_url).netloc == urlparse(url).netloc


def is_http_url(
    url: str,
):


    scheme = urlparse(url).scheme.lower()

    return scheme in (
        "http",
        "https",
    )


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


def extension_filter(
    url: str,
):


    path = urlparse(url).path.lower()

    return not any(path.endswith(extension) for extension in IGNORED_EXTENSIONS)


def robots_filter(
    url: str,
    rules: list[str],
):


    if not rules:

        return True

    path = urlparse(url).path

    for rule in rules:

        if rule and path.startswith(rule):

            return False

    return True


def duplicate_filter(
    url: str,
    visited: set,
):


    return url not in visited


def depth_filter(
    depth: int,
    max_depth: int,
):


    return depth <= max_depth


def should_enqueue(
    root_url: str,
    url: str,
    visited: set,
    robots_rules: list[str],
    depth: int,
    max_depth: int,
):


    url = normalize_url(url)

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


def should_crawl(
    url: str,
    visited: set,
):


    url = normalize_url(url)

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


def normalize_urls(
    urls: list[str],
):


    normalized = {normalize_url(url) for url in urls if is_http_url(url)}

    return sorted(normalized)
