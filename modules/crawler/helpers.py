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

import urllib3

urllib3.disable_warnings(

    urllib3.exceptions.InsecureRequestWarning

)

import requests

from requests.exceptions import (

    ConnectionError,

    ConnectTimeout,

    HTTPError,

    ReadTimeout,

    Timeout,

)

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
# Retryable HTTP Status Codes
# ==========================================================

RETRY_STATUS_CODES = {

    500,

    502,

    503,

    504,

}


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
# Retry Policy
# ==========================================================

def should_retry(
    error: Exception,
):
    """
    Decide whether a request
    should be retried.
    """

    if isinstance(

        error,

        (

            Timeout,

            ConnectTimeout,

            ReadTimeout,

            ConnectionError,

        ),

    ):

        return True

    if isinstance(

        error,

        HTTPError,

    ):

        response = getattr(

            error,

            "response",

            None,

        )

        if response is None:

            return False

        return (

            response.status_code

            in

            RETRY_STATUS_CODES

        )

    return False


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

                f"SSL Error: {url} ({error})"

            )

            return None

        except requests.RequestException as error:

            if not should_retry(

                error

            ):

                if isinstance(

                    error,

                    HTTPError,

                ) and error.response is not None:

                    debug(

                        f"HTTP {error.response.status_code}: {url}"

                    )

                else:

                    debug(

                        f"Not retrying: {url} ({error})"

                    )

                return None

            if isinstance(

                error,

                HTTPError,

            ) and error.response is not None:

                debug(

                    f"Retry "

                    f"({attempt + 1}/{CRAWLER_RETRIES}) "

                    f"HTTP {error.response.status_code}: "

                    f"{url}"

                )

            else:

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

    Returns:
        str
    """

    return urlparse(

        url

    ).netloc