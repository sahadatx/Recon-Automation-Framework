import json
from pathlib import Path

from core.logger import warning


def load_json(
    file: Path,
) -> dict | None:


    try:

        with file.open(
            "r",
            encoding="utf-8",
        ) as handle:

            return json.load(handle)

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:

        warning(f"Unable to parse {file}: {error}")

        return None


def parse_results(
    results: list,
) -> list:


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


def parse_ffuf(
    file: Path,
) -> dict | None:


    data = load_json(file)

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


def validate_json(
    file: Path,
) -> bool:


    data = load_json(file)

    return data is not None and "results" in data
