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

    HTTP_USER_AGENT,

    HTTP_VERIFY_SSL,

    CRAWLER_RETRIES,

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

            "User-Agent": HTTP_USER_AGENT,

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
    Check whether two URLs
    belong to the same host.

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
# HTML Detection
# ==========================================================

def is_html(
    response,
):
    """
    Check whether response
    contains HTML.

    Returns:
        bool
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

    Args:
        url:
            Target URL.

    Returns:
        requests.Response | None
    """

    for attempt in range(

        CRAWLER_RETRIES

    ):

        try:

            response = SESSION.get(

                url,

                timeout=HTTP_TIMEOUT,

                allow_redirects=True,

                verify=HTTP_VERIFY_SSL,

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

        except requests.exceptions.SSLError as error:

            debug(

                f"SSL Error "

                f"({attempt + 1}/{CRAWLER_RETRIES}): "

                f"{url} ({error})"

            )

        except requests.RequestException as error:

            debug(

                f"Retry "

                f"({attempt + 1}/{CRAWLER_RETRIES}): "

                f"{url} ({error})"

            )

    debug(

        f"Failed after "

        f"{CRAWLER_RETRIES} attempts: "

        f"{url}"

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

    Args:
        url:
            Target URL.

    Returns:
        str
    """

    return urlparse(
        url
    ).netloc