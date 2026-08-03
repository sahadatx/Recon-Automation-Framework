"""
WAF Scanner

Collect HTTP response data for
WAF fingerprint detection.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from requests.exceptions import ConnectionError, RequestException, Timeout

from config.config import HTTP_TIMEOUT, HTTP_VERIFY_SSL
from core.context import ExecutionContext

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
    context: ExecutionContext,
    url: str,
) -> dict[str, Any]:
    """
    Collect HTTP response data.

    Returns:
        HTTP response information.
    """

    session = context.get_http_session()

    if session is None:
        raise RuntimeError("Shared HTTP session is not initialized.")

    result = deepcopy(
        EMPTY_RESULT,
    )

    result["url"] = url

    try:

        response = session.get(
            url,
            timeout=HTTP_TIMEOUT,
            verify=HTTP_VERIFY_SSL,
            allow_redirects=True,
        )

        result["status"] = response.status_code

        result["headers"] = {
            key.lower(): value for key, value in response.headers.items()
        }

        result["cookies"] = {
            key.lower(): value for key, value in response.cookies.items()
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
    ) as error:

        result["error"] = str(
            error,
        )

    except RequestException as error:

        result["error"] = str(
            error,
        )

    except Exception as error:

        result["error"] = str(
            error,
        )

    return result


# ==========================================================
# Scan Multiple Targets
# ==========================================================


def scan_targets(
    context: ExecutionContext,
    targets: list[str],
) -> list[dict[str, Any]]:
    """
    Scan multiple targets.

    Returns:
        List of scan results.
    """

    results: list[dict[str, Any]] = []

    total = len(
        targets,
    )

    for index, target in enumerate(
        targets,
        start=1,
    ):

        print(
            f"[{index}/{total}] " f"Scanning {target}",
        )

        results.append(
            scan_target(
                context,
                target,
            ),
        )

    return results


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "scan_target",
    "scan_targets",
]
