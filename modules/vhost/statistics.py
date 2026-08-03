"""
Virtual Host Discovery Statistics

Generate summary statistics
for Virtual Host Discovery.
"""

from __future__ import annotations

from typing import Any

# ==========================================================
# Count Status Code
# ==========================================================


def count_status(
    results: list[dict[str, Any]],
    status: int,
) -> int:
    """
    Count HTTP status code.

    Args:
        results:
            Virtual host results.

        status:
            HTTP status code.

    Returns:
        Number of matching responses.
    """

    return sum(
        1
        for result in results
        if result.get(
            "status",
            0,
        )
        == status
    )


# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    results: list[dict[str, Any]],
    interesting: list[dict[str, Any]],
) -> dict[str, Any]:
    """
    Generate Virtual Host Discovery statistics.

    Args:
        results:
            Discovered virtual hosts.

        interesting:
            Interesting virtual hosts.

    Returns:
        Summary statistics.
    """

    return {
        "total_results": len(results),
        "interesting_hosts": len(interesting),
        "status_200": count_status(
            results,
            200,
        ),
        "status_204": count_status(
            results,
            204,
        ),
        "status_301": count_status(
            results,
            301,
        ),
        "status_302": count_status(
            results,
            302,
        ),
        "status_307": count_status(
            results,
            307,
        ),
        "status_401": count_status(
            results,
            401,
        ),
        "status_403": count_status(
            results,
            403,
        ),
    }


# ==========================================================
# Empty Statistics
# ==========================================================


def empty_statistics() -> dict[str, Any]:
    """
    Return empty Virtual Host Discovery statistics.

    Returns:
        Empty statistics dictionary.
    """

    return {
        "total_results": 0,
        "interesting_hosts": 0,
        "status_200": 0,
        "status_204": 0,
        "status_301": 0,
        "status_302": 0,
        "status_307": 0,
        "status_401": 0,
        "status_403": 0,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
    "empty_statistics",
]
