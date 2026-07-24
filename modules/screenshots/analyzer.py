"""
Screenshot Analyzer

Analyze screenshot capture results
and generate final analysis report.
"""

from __future__ import annotations

from modules.screenshots.statistics import (
    generate_statistics,
)


# ==========================================================
# Analyze Screenshot Results
# ==========================================================

def analyze(
    results: list[dict],
    elapsed: float,
) -> dict:
    """
    Analyze screenshot results.

    Args:
        results:
            Screenshot capture results.

        elapsed:
            Total screenshot scan time.

    Returns:
        Complete screenshot analysis.
    """

    statistics = generate_statistics(
        results
    )


    return {

        "total_targets": statistics[

            "total_targets"

        ],

        "captured": statistics[

            "captured"

        ],

        "failed": statistics[

            "failed"

        ],

        "success_rate": statistics[

            "success_rate"

        ],

        "scan_time": elapsed,

        "results": results,

        "statistics": statistics,

    }


# ==========================================================
# Filter Successful Screenshots
# ==========================================================

def get_successful_screenshots(
    analysis: dict,
) -> list[dict]:
    """
    Return captured screenshots.

    Returns:
        list
    """

    return [

        result

        for result

        in analysis.get(

            "results",

            []

        )

        if result.get(

            "captured",

            False,

        )

    ]


# ==========================================================
# Filter Failed Screenshots
# ==========================================================

def get_failed_screenshots(
    analysis: dict,
) -> list[dict]:
    """
    Return failed screenshots.

    Returns:
        list
    """

    return [

        result

        for result

        in analysis.get(

            "results",

            []

        )

        if not result.get(

            "captured",

            False,

        )

    ]


# ==========================================================
# Build Dashboard Data
# ==========================================================

def dashboard_data(
    analysis: dict,
) -> dict:
    """
    Prepare dashboard friendly data.

    Returns:
        dict
    """

    statistics = analysis.get(
        "statistics",
        {},
    )


    return {

        "summary": {

            "total": statistics.get(

                "total_targets",

                0,

            ),

            "captured": statistics.get(

                "captured",

                0,

            ),

            "failed": statistics.get(

                "failed",

                0,

            ),

            "success_rate": statistics.get(

                "success_rate",

                0,

            ),

        },


        "performance": {

            "scan_time": analysis.get(

                "scan_time",

                0,

            ),

            "average_time": statistics.get(

                "average_time",

                0,

            ),

            "average_size": statistics.get(

                "average_size",

                0,

            ),

        },


        "status_codes": statistics.get(

            "status_codes",

            {},

        ),

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "analyze",

    "get_successful_screenshots",

    "get_failed_screenshots",

    "dashboard_data",

]