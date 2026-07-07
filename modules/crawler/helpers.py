"""
Crawler Helper Functions

Shared helper functions used by the
URL Discovery module.
"""

from urllib.parse import (
    urljoin,
    urlparse,
    urlunparse,
)

import requests

from config.config import (
    HTTP_TIMEOUT,
)

from core.logger import (
    debug,
)


# ==========================================================
# Create Session
# ==========================================================

def create_session():
    """
    Create reusable HTTP session.

    Returns:
        requests.Session
    """

    session = requests.Session()

    session.headers.update(

        {

            "User-Agent": (
                "ReconAutomationFramework/2.0"
            ),

            "Accept": (
                "text/html,"
                "application/xhtml+xml,"
                "application/xml;q=0.9,*/*;q=0.8"
            ),

            "Accept-Encoding": (
                "gzip, deflate, br"
            ),

            "Connection": "keep-alive",

        }

    )

    return session


# ==========================================================
# Global Session
# ==========================================================

SESSION = create_session()


# ==========================================================
# Normalize URL
# ==========================================================

def normalize_url(
    base_url: str,
    link: str,
):
    """
    Convert relative URL into
    canonical absolute URL.

    Returns:
        str
    """

    url = urljoin(
        base_url,
        link,
    )

    parsed = urlparse(
        url
    )

    path = parsed.path

    if path == "/":

        path = ""

    elif path.endswith("/"):

        path = path.rstrip("/")

    parsed = parsed._replace(

        path=path,

        fragment="",

    )

    return urlunparse(
        parsed
    )


# ==========================================================
# Same Domain
# ==========================================================

def same_domain(
    root_url: str,
    url: str,
):
    """
    Check same hostname.
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
# Is HTML
# ==========================================================

def is_html(
    response,
):
    """
    Check whether response
    is HTML.
    """

    if response is None:

        return False

    content_type = response.headers.get(

        "Content-Type",

        "",

    ).lower()

    return (

        "text/html"

        in

        content_type

        or

        "application/xhtml+xml"

        in

        content_type

    )


# ==========================================================
# Download Page
# ==========================================================

def download_page(
    url: str,
):
    """
    Download HTML page.

    Returns:
        requests.Response | None
    """

    for attempt in range(3):

        try:

            response = SESSION.get(

                url,

                timeout=HTTP_TIMEOUT,

                allow_redirects=True,

            )

            response.raise_for_status()

            if not is_html(
                response
            ):

                debug(
                    f"Skipped non-HTML: {url}"
                )

                return None

            return response

        except requests.RequestException as error:

            debug(
                f"Retry {attempt + 1}: {url} ({error})"
            )

    debug(
        f"Failed: {url}"
    )

    return None


# ==========================================================
# Extract Domain
# ==========================================================

def get_domain(
    url: str,
):
    """
    Return hostname.
    """

    return urlparse(
        url
    ).netloc