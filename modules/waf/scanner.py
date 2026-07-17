"""
WAF Scanner

Collect HTTP response data for
WAF fingerprint detection.
"""

from __future__ import annotations

from copy import deepcopy

from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import (
    ConnectionError,
    RequestException,
    Timeout,
)
from urllib3.util.retry import Retry

from config.config import (
    HTTP_TIMEOUT,
    HTTP_USER_AGENT,
    HTTP_VERIFY_SSL,
)

# ==========================================================
# HTTP Session
# ==========================================================

SESSION = Session()

retry = Retry(

    total=2,

    connect=2,

    read=2,

    backoff_factor=0.5,

    status_forcelist=(

        500,
        502,
        503,
        504,

    ),

    allowed_methods=(

        "GET",

        "HEAD",

    ),

)

adapter = HTTPAdapter(

    max_retries=retry,

)

SESSION.mount(

    "http://",

    adapter,

)

SESSION.mount(

    "https://",

    adapter,

)

SESSION.headers.update(

    {

        "User-Agent": HTTP_USER_AGENT,

        "Accept": "*/*",

        "Accept-Language": "en-US,en;q=0.9",

    }

)

# ==========================================================
# Empty Result
# ==========================================================

EMPTY_RESULT = {

    "url": "",

    "status": None,

    "headers": {},

    "cookies": {},

    "server": "",

    "body": "",

    "response_time": 0.0,

    "error": None,

}

# ==========================================================
# Scan Target
# ==========================================================

def scan_target(
    url: str,
):
    """
    Collect HTTP response data.

    Returns:
        dict
    """

    result = deepcopy(

        EMPTY_RESULT

    )

    result["url"] = url

    try:

        response = SESSION.get(

            url,

            timeout=HTTP_TIMEOUT,

            verify=HTTP_VERIFY_SSL,

            allow_redirects=True,

        )

        result["status"] = response.status_code

        result["headers"] = {

            key.lower(): value

            for key, value

            in response.headers.items()

        }

        result["cookies"] = {

            key.lower(): value

            for key, value

            in response.cookies.items()

        }

        result["server"] = response.headers.get(

            "Server",

            "",

        ).lower()

        result["body"] = response.text[:8192].lower()

        result["response_time"] = round(

            response.elapsed.total_seconds(),

            3,

        )

    except (

        Timeout,

        ConnectionError,

    ) as exc:

        result["error"] = str(

            exc

        )

    except RequestException as exc:

        result["error"] = str(

            exc

        )

    except Exception as exc:

        result["error"] = str(

            exc

        )

    return result


# ==========================================================
# Scan Multiple Targets
# ==========================================================

def scan_targets(
    targets,
):
    """
    Scan multiple targets.

    Returns:
        list
    """

    results = []

    total = len(

        targets

    )

    for index, target in enumerate(

        targets,

        start=1,

    ):

        print(

            f"[{index}/{total}] Scanning {target}"

        )

        results.append(

            scan_target(

                target

            )

        )

    return results