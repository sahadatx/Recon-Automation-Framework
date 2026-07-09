"""
Directory Fuzzing Statistics

Generates statistics for
directory fuzzing results.
"""


# ==========================================================
# Status Code Statistics
# ==========================================================

def status_statistics(
    results: list,
):
    """
    Count HTTP status codes.

    Returns:
        dict
    """

    statistics = {}

    for result in results:

        status = str(

            result.get(
                "status",
                0,
            )

        )

        statistics[status] = (

            statistics.get(
                status,
                0,
            )

            + 1

        )

    return dict(

        sorted(
            statistics.items()
        )

    )


# ==========================================================
# Response Size Statistics
# ==========================================================

def response_statistics(
    results: list,
):
    """
    Generate response statistics.

    Returns:
        dict
    """

    if not results:

        return {

            "minimum": 0,

            "maximum": 0,

            "average": 0,

        }

    sizes = [

        result.get(
            "length",
            0,
        )

        for result in results

    ]

    return {

        "minimum": min(
            sizes
        ),

        "maximum": max(
            sizes
        ),

        "average": round(

            sum(sizes)

            / len(sizes),

            2,

        ),

    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results: list,
    interesting: dict,
):
    """
    Generate overall statistics.

    Returns:
        dict
    """

    interesting_stats = interesting.get(

        "statistics",

        {},

    )

    return {

        "total_results": len(
            results
        ),

        "status_codes": status_statistics(
            results
        ),

        "responses": response_statistics(
            results
        ),

        "interesting_files": interesting_stats.get(

            "interesting_files",

            0,

        ),

        "interesting_directories": interesting_stats.get(

            "interesting_directories",

            0,

        ),

        "interesting_total": interesting_stats.get(

            "total",

            0,

        ),

    }


# ==========================================================
# Entry Point
# ==========================================================

def generate(
    results: list,
    interesting: dict,
):
    """
    Entry point.

    Args:
        results:
            Filtered ffuf results.

        interesting:
            Interesting findings.

    Returns:
        dict
    """

    return generate_statistics(

        results,

        interesting,

    )