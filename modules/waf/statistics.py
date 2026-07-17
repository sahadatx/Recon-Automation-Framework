"""
WAF Statistics

Generate statistics for
WAF Detection.
"""

from __future__ import annotations

from collections import Counter


# ==========================================================
# Vendor Statistics
# ==========================================================

def vendor_statistics(results):
    """
    Count detected vendors.

    Returns:
        dict
    """

    vendors = [

        result["vendor"]

        for result

        in results

        if result.get(

            "vendor"

        )

    ]

    return dict(

        sorted(

            Counter(

                vendors

            ).items(),

            key=lambda item: (

                -item[1],

                item[0],

            ),

        )

    )


# ==========================================================
# Confidence Statistics
# ==========================================================

def confidence_statistics(results):
    """
    Count confidence levels.

    Returns:
        dict
    """

    order = [

        "High",

        "Medium",

        "Low",

        "Unknown",

    ]

    counter = Counter(

        result.get(

            "confidence",

            "Unknown",

        )

        for result

        in results

    )

    return {

        level: counter[level]

        for level

        in order

        if counter[level]

    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results,
    elapsed=0.0,
):
    """
    Generate statistics.

    Returns:
        dict
    """

    total = len(

        results

    )

    detected = sum(

        result.get(

            "detected",

            False,

        )

        for result

        in results

    )

    scores = [

        result.get(

            "score",

            0,

        )

        for result

        in results

    ]

    average_score = round(

        sum(

            scores

        )

        / total,

        2,

    ) if total else 0.0

    highest_score = max(

        scores,

        default=0,

    )

    return {

        "targets": total,

        "detected": detected,

        "not_detected": total - detected,

        "success_rate": round(

            (

                detected

                / total

                * 100

            ),

            2,

        ) if total else 0.0,

        "average_score": average_score,

        "highest_score": highest_score,

        "vendors": vendor_statistics(

            results

        ),

        "confidence": confidence_statistics(

            results

        ),

        "elapsed": round(

            elapsed,

            2,

        ),

    }


# ==========================================================
# Print Summary
# ==========================================================

def print_summary(statistics):
    """
    Print summary.
    """

    print()

    print("=" * 80)

    print(

        "WAF Detection Summary".center(

            80

        )

    )

    print("=" * 80)

    print(

        f"Targets             : {statistics['targets']}"

    )

    print(

        f"WAF Detected        : {statistics['detected']}"

    )

    print(

        f"Not Detected        : {statistics['not_detected']}"

    )

    print(

        f"Success Rate        : {statistics['success_rate']}%"

    )

    print(

        f"Average Score       : {statistics['average_score']}"

    )

    print(

        f"Highest Score       : {statistics['highest_score']}"

    )

    print(

        f"Elapsed Time        : {statistics['elapsed']} sec"

    )

    print("-" * 80)

    print("Detected Vendors")

    print("-" * 80)

    if statistics["vendors"]:

        for vendor, count in statistics["vendors"].items():

            print(

                f"{vendor:<30}{count}"

            )

    else:

        print(

            "None"

        )

    print("-" * 80)

    print("Confidence Levels")

    print("-" * 80)

    if statistics["confidence"]:

        for level, count in statistics["confidence"].items():

            print(

                f"{level:<30}{count}"

            )

    else:

        print(

            "None"

        )

    print("=" * 80)