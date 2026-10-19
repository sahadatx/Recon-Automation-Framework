import json
from pathlib import Path


def read_json(
    filepath: str | Path,
):


    path = Path(filepath)

    if not path.exists():

        return None

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception:

        return None


def normalize_result(
    result: dict,
):


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


def parse_results(
    data: dict,
):


    return [
        normalize_result(item)
        for item in data.get(
            "results",
            [],
        )
    ]


def parse_file(
    filepath: str | Path,
):


    data = read_json(filepath)

    if data is None:

        return None

    return {"results": parse_results(data)}


def parse_ffuf(
    filepath: str | Path,
):


    return parse_file(filepath)
