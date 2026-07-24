"""
Screenshot Statistics

Generate statistics for screenshot
capture results.
"""

from __future__ import annotations


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results: list[dict],
) -> dict:
    """
    Generate screenshot statistics.

    Args:
        results:
            Screenshot capture results.

    Returns:
        dict
    """

    total = len(
        results
    )

    captured = 0

    failed = 0

    total_size = 0

    total_time = 0.0

    status_codes: dict[str, int] = {}

    successful_urls: list[str] = []

    failed_urls: list[str] = []


    for result in results:

        if result.get(
            "captured",
            False,
        ):

            captured += 1

            url = result.get(
                "url"
            )

            if url:

                successful_urls.append(
                    url
                )

            total_size += result.get(
                "filesize",
                0,
            )

            total_time += result.get(
                "elapsed",
                0.0,
            )


            status = result.get(
                "status"
            )

            if status:

                status = str(
                    status
                )

                status_codes[status] = (
                    status_codes.get(
                        status,
                        0,
                    )
                    + 1
                )


        else:

            failed += 1

            url = result.get(
                "url"
            )

            if url:

                failed_urls.append(
                    url
                )


    average_time = 0.0

    if captured:

        average_time = round(

            total_time / captured,

            2,

        )


    average_size = 0

    if captured:

        average_size = round(

            total_size / captured,

            2,

        )


    return {

        "total_targets": total,

        "captured": captured,

        "failed": failed,

        "success_rate": (

            round(

                (captured / total) * 100,

                2,

            )

            if total

            else 0.0

        ),

        "total_size": total_size,

        "average_size": average_size,

        "average_time": average_time,

        "status_codes": status_codes,

        "successful_urls": successful_urls,

        "failed_urls": failed_urls,

    }


# ==========================================================
# Capture Summary
# ==========================================================

def generate_summary(
    results: list[dict],
) -> dict:
    """
    Generate human readable summary data.

    Returns:
        dict
    """

    statistics = generate_statistics(
        results
    )

    return {

        "screenshots": statistics[
            "captured"
        ],

        "failed": statistics[
            "failed"
        ],

        "success_rate": statistics[
            "success_rate"
        ],

        "average_time": statistics[
            "average_time"
        ],

        "average_size": statistics[
            "average_size"
        ],

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "generate_statistics",

    "generate_summary",

]