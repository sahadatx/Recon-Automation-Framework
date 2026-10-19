from __future__ import annotations

from copy import deepcopy


MAX_SCORE = 100

VALID_CONFIDENCE = {
    "High",
    "Medium",
    "Low",
    "Unknown",
}


def reset_detection(
    result: dict,
):


    result["vendor"] = None
    result["detected"] = False
    result["score"] = 0
    result["confidence"] = "Unknown"
    result["evidence"] = []

    return result


def normalize_score(
    score: int,
):


    return max(
        0,
        min(
            score,
            MAX_SCORE,
        ),
    )


def normalize_evidence(
    evidence,
):


    return sorted({item.strip() for item in evidence if item})


def validate_confidence(
    confidence,
):


    if confidence in VALID_CONFIDENCE:

        return confidence

    return "Unknown"


def has_evidence(
    evidence,
    prefix,
):


    return any(item.startswith(prefix) for item in evidence)


def validate_result(
    result,
):


    if not result.get("vendor"):

        return reset_detection(result)

    if not result.get("evidence"):

        return reset_detection(result)

    result["confidence"] = validate_confidence(
        result.get(
            "confidence",
            "Unknown",
        )
    )

    return result


def remove_false_positive(
    result,
):


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


    if (body or status) and not (header or cookie or server):

        return reset_detection(result)

    return result


def filter_result(
    result,
):


    filtered = deepcopy(result)

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

    filtered = validate_result(filtered)

    filtered = remove_false_positive(filtered)

    return filtered


def filter_results(
    results,
):


    filtered = [filter_result(result) for result in results]

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
            )
            or "",
        ),
        reverse=True,
    )

    return filtered


def detected_only(
    results,
):


    return [
        result
        for result in results
        if result.get(
            "detected",
            False,
        )
    ]


def remove_unknown(
    results,
):


    return [result for result in results if result.get("vendor")]
