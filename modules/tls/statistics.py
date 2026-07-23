"""
TLS Statistics

Generate statistics for
TLS Analysis.
"""

from __future__ import annotations

from collections import Counter


# ==========================================================
# Risk Level Statistics
# ==========================================================

def risk_level_statistics(
    results,
):
    """
    Count risk levels.

    Returns:
        dict
    """

    order = [

        "Critical",

        "High",

        "Medium",

        "Low",

        "Safe",

    ]

    counter = Counter(

        result.get(

            "risk_level",

            "Safe",

        )

        for result

        in results

    )

    return {

        level: counter[level]

        for level

        in order

    }


# ==========================================================
# Security Statistics
# ==========================================================

def security_statistics(
    results,
):
    """
    Count security findings.

    Returns:
        dict
    """

    return {

        "expired": sum(

            result.get(

                "expired",

                False,

            )

            for result

            in results

        ),

        "self_signed": sum(

            result.get(

                "self_signed",

                False,

            )

            for result

            in results

        ),

        "hostname_mismatch": sum(

            not result.get(

                "hostname_match",

                True,

            )

            for result

            in results

        ),

        "weak_protocol": sum(

            result.get(

                "weak_protocol",

                False,

            )

            for result

            in results

        ),

        "weak_cipher": sum(

            result.get(

                "weak_cipher",

                False,

            )

            for result

            in results

        ),

        "wildcard": sum(

            result.get(

                "wildcard",

                False,

            )

            for result

            in results

        ),

        "forward_secrecy": sum(

            result.get(

                "forward_secrecy",

                False,

            )

            for result

            in results

        ),

    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results,
    elapsed=0.0,
):
    """
    Generate TLS statistics.

    Returns:
        dict
    """

    total = len(

        results

    )

    scores = [

        result.get(

            "risk_score",

            0,

        )

        for result

        in results

    ]

    average_risk = round(

        sum(

            scores

        )

        / total,

        2,

    ) if total else 0.0

    highest_risk = max(

        scores,

        default=0,

    )

    statistics = security_statistics(

        results,

    )

    return {

        "targets": total,

        "risk_levels": risk_level_statistics(

            results,

        ),

        "average_risk": average_risk,

        "highest_risk": highest_risk,

        "expired": statistics["expired"],

        "self_signed": statistics["self_signed"],

        "hostname_mismatch": statistics["hostname_mismatch"],

        "weak_protocol": statistics["weak_protocol"],

        "weak_cipher": statistics["weak_cipher"],

        "wildcard": statistics["wildcard"],

        "forward_secrecy": statistics["forward_secrecy"],

        "elapsed": round(

            elapsed,

            2,

        ),

    }


# ==========================================================
# Print Summary
# ==========================================================

def print_summary(
    statistics,
):
    """
    Print TLS summary.
    """

    print()

    print("=" * 80)

    print(

        "TLS Analysis Summary".center(

            80,

        )

    )

    print("=" * 80)

    print(

        f"Targets             : {statistics['targets']}"

    )

    print(

        f"Average Risk        : {statistics['average_risk']}"

    )

    print(

        f"Highest Risk        : {statistics['highest_risk']}"

    )

    print(

        f"Expired             : {statistics['expired']}"

    )

    print(

        f"Self Signed         : {statistics['self_signed']}"

    )

    print(

        f"Hostname Mismatch   : {statistics['hostname_mismatch']}"

    )

    print(

        f"Weak Protocol       : {statistics['weak_protocol']}"

    )

    print(

        f"Weak Cipher         : {statistics['weak_cipher']}"

    )

    print(

        f"Wildcard            : {statistics['wildcard']}"

    )

    print(

        f"Forward Secrecy     : {statistics['forward_secrecy']}"

    )

    print(

        f"Elapsed Time        : {statistics['elapsed']} sec"

    )

    print("-" * 80)

    print("Risk Levels")

    print("-" * 80)

    if statistics["risk_levels"]:

        for level, count in statistics["risk_levels"].items():

            print(

                f"{level:<30}{count}"

            )

    else:

        print(

            "None"

        )

    print("=" * 80)


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "risk_level_statistics",

    "security_statistics",

    "generate_statistics",

    "print_summary",

]

