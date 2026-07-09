"""
Directory Fuzzing Parser

Parses ffuf JSON output into
normalized Python objects.
"""

import json
from pathlib import Path


# ==========================================================
# Read JSON
# ==========================================================

def read_json(
    filepath: str | Path,
):
    """
    Read ffuf JSON output.

    Args:
        filepath:
            JSON output file.

    Returns:
        dict | None
    """

    path = Path(
        filepath
    )

    if not path.exists():

        return None

    try:

        with path.open(

            "r",

            encoding="utf-8",

        ) as file:

            return json.load(
                file
            )

    except Exception:

        return None


# ==========================================================
# Normalize Result
# ==========================================================

def normalize_result(
    result: dict,
):
    """
    Normalize one ffuf result.

    Args:
        result:
            Raw ffuf result.

    Returns:
        dict
    """

    return {

        "url": result.get(
            "url",
            "",
        ),

        "status": result.get(
            "status",
            0,
        ),

        "length": result.get(
            "length",
            0,
        ),

        "words": result.get(
            "words",
            0,
        ),

        "lines": result.get(
            "lines",
            0,
        ),

        "content_type": result.get(
            "content-type",
            "",
        ),

        "redirect": result.get(
            "redirectlocation",
            "",
        ),

    }


# ==========================================================
# Parse Results
# ==========================================================

def parse_results(
    data: dict,
):
    """
    Parse ffuf results.

    Args:
        data:
            Loaded JSON.

    Returns:
        list
    """

    return [

        normalize_result(
            item
        )

        for item in data.get(
            "results",
            [],
        )

    ]


# ==========================================================
# Parse File
# ==========================================================

def parse_file(
    filepath: str | Path,
):
    """
    Parse ffuf JSON file.

    Args:
        filepath:
            JSON output file.

    Returns:
        dict | None
    """

    data = read_json(
        filepath
    )

    if data is None:

        return None

    return {

        "results": parse_results(
            data
        )

    }


# ==========================================================
# Entry Point
# ==========================================================

def parse_ffuf(
    filepath: str | Path,
):
    """
    Entry point.

    Args:
        filepath:
            ffuf JSON output.

    Returns:
        dict | None
    """

    return parse_file(
        filepath
    )