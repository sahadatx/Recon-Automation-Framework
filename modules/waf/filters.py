"""
WAF Filters

Filter and normalize
WAF detection results.
"""

from __future__ import annotations

from copy import deepcopy

# ==========================================================
# Constants
# ==========================================================

MAX_SCORE = 100

VALID_CONFIDENCE = {

    "High",
    "Medium",
    "Low",
    "Unknown",

}

# ==========================================================
# Reset Detection
# ==========================================================

def reset_detection(
    result: dict,
):
    """
    Reset invalid detection.

    Returns:
        dict
    """

    result["vendor"] = None
    result["detected"] = False
    result["score"] = 0
    result["confidence"] = "Unknown"
    result["evidence"] = []

    return result


# ==========================================================
# Normalize Score
# ==========================================================

def normalize_score(
    score: int,
):
    """
    Normalize score.

    Returns:
        int
    """

    return max(

        0,

        min(

            score,

            MAX_SCORE,

        ),

    )


# ==========================================================
# Normalize Evidence
# ==========================================================

def normalize_evidence(
    evidence,
):
    """
    Normalize evidence.

    Returns:
        list
    """

    return sorted(

        {

            item.strip()

            for item

            in evidence

            if item

        }

    )


# ==========================================================
# Validate Confidence
# ==========================================================

def validate_confidence(
    confidence,
):
    """
    Validate confidence level.

    Returns:
        str
    """

    if confidence in VALID_CONFIDENCE:

        return confidence

    return "Unknown"


# ==========================================================
# Has Evidence Type
# ==========================================================

def has_evidence(
    evidence,
    prefix,
):
    """
    Check evidence type.

    Returns:
        bool
    """

    return any(

        item.startswith(

            prefix

        )

        for item

        in evidence

    )


# ==========================================================
# Validate Result
# ==========================================================

def validate_result(
    result,
):
    """
    Validate detection result.

    Returns:
        dict
    """

    if not result.get(

        "vendor"

    ):

        return reset_detection(

            result

        )

    if not result.get(

        "evidence"

    ):

        return reset_detection(

            result

        )

    result["confidence"] = validate_confidence(

        result.get(

            "confidence",

            "Unknown",

        )

    )

    return result


# ==========================================================
# False Positive Filter
# ==========================================================

def remove_false_positive(
    result,
):
    """
    Remove weak detections.

    Returns:
        dict
    """

    evidence = result.get(

        "evidence",

        [],

    )

    header = has_evidence(

        evidence,

        "Header:",

    )

    cookie = has_evidence(

        evidence,

        "Cookie:",

    )

    server = has_evidence(

        evidence,

        "Server:",

    )

    body = has_evidence(

        evidence,

        "Body:",

    )

    status = has_evidence(

        evidence,

        "Status:",

    )

    # Only body or only status

    if (

        body

        or status

    ) and not (

        header

        or cookie

        or server

    ):

        return reset_detection(

            result

        )

    return result


# ==========================================================
# Filter Single Result
# ==========================================================

def filter_result(
    result,
):
    """
    Filter one result.

    Returns:
        dict
    """

    filtered = deepcopy(

        result

    )

    filtered["score"] = normalize_score(

        filtered.get(

            "score",

            0,

        )

    )

    filtered["evidence"] = normalize_evidence(

        filtered.get(

            "evidence",

            [],

        )

    )

    filtered = validate_result(

        filtered

    )

    filtered = remove_false_positive(

        filtered

    )

    return filtered


# ==========================================================
# Filter Results
# ==========================================================

def filter_results(
    results,
):
    """
    Filter all results.

    Returns:
        list
    """

    filtered = [

        filter_result(

            result

        )

        for result

        in results

    ]

    filtered.sort(

        key=lambda item: (

            item.get(

                "detected",

                False,

            ),

            item.get(

                "score",

                0,

            ),

            item.get(

                "vendor",

            ) or "",

        ),

        reverse=True,

    )

    return filtered


# ==========================================================
# Detected Only
# ==========================================================

def detected_only(
    results,
):
    """
    Return detected results.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if result.get(

            "detected",

            False,

        )

    ]


# ==========================================================
# Remove Unknown
# ==========================================================

def remove_unknown(
    results,
):
    """
    Remove unknown vendors.

    Returns:
        list
    """

    return [

        result

        for result

        in results

        if result.get(

            "vendor"

        )

    ]