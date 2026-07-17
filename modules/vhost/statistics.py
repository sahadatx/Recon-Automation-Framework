"""
Virtual Host Discovery Statistics

Generate summary statistics
for Virtual Host Discovery.
"""


# ==========================================================
# Count Status Codes
# ==========================================================

def count_status(
    results: list,
    status: int,
) -> int:
    """
    Count HTTP status code.

    Args:
        results:
            Parsed results.

        status:
            HTTP status code.

    Returns:
        int
    """

    return sum(

        1

        for result in results

        if result.get(

            "status",

            0,

        ) == status

    )


# ==========================================================
# Generate Statistics
# ==========================================================

def generate(
    results: list,
    interesting: list,
) -> dict:
    """
    Generate summary statistics.

    Args:
        results:
            Filtered results.

        interesting:
            Interesting hosts.

    Returns:
        dict
    """

    return {

        "total_results": len(

            results

        ),

        "interesting_hosts": len(

            interesting

        ),

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

def empty() -> dict:
    """
    Return empty statistics.

    Returns:
        dict
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