"""
Virtual Host Discovery Parser

Parses ffuf JSON output
into a normalized format.
"""

import json

from pathlib import Path

from core.logger import (
    warning,
)


# ==========================================================
# Load JSON
# ==========================================================

def load_json(
    file: Path,
) -> dict | None:
    """
    Load ffuf JSON file.

    Args:
        file:
            JSON output file.

    Returns:
        dict | None
    """

    try:

        with file.open(

            "r",

            encoding="utf-8",

        ) as handle:

            return json.load(
                handle
            )

    except (

        OSError,

        json.JSONDecodeError,

    ) as error:

        warning(

            f"Unable to parse {file}: {error}"

        )

        return None


# ==========================================================
# Parse Results
# ==========================================================

def parse_results(
    results: list,
) -> list:
    """
    Normalize ffuf results.

    Args:
        results:
            Raw ffuf results.

    Returns:
        list
    """

    parsed = []

    for result in results:

        parsed.append(

            {

                "host": result.get(

                    "input",

                    {},

                ).get(

                    "FUZZ",

                    "",

                ),

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

                "redirect": result.get(

                    "redirectlocation",

                    "",

                ),

            }

        )

    return parsed


# ==========================================================
# Parse ffuf Output
# ==========================================================

def parse_ffuf(
    file: Path,
) -> dict | None:
    """
    Parse ffuf JSON output.

    Args:
        file:
            ffuf JSON file.

    Returns:
        dict | None
    """

    data = load_json(
        file
    )

    if data is None:

        return None

    return {

        "commandline": data.get(

            "commandline",

            "",

        ),

        "time": data.get(

            "time",

            "",

        ),

        "results": parse_results(

            data.get(

                "results",

                [],

            )

        ),

    }


# ==========================================================
# JSON Validation
# ==========================================================

def validate_json(
    file: Path,
) -> bool:
    """
    Validate ffuf JSON.

    Args:
        file:
            JSON output.

    Returns:
        bool
    """

    data = load_json(
        file
    )

    return (

        data is not None

        and

        "results" in data

    )