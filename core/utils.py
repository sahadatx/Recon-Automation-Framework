"""
Utility Functions

Shared helper functions used throughout the framework.
"""

import re
import time
from pathlib import Path


def create_directory(directory: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory: Directory path.
    """

    Path(directory).mkdir(
        parents=True,
        exist_ok=True
    )


def read_file(file_path: str) -> list[str]:
    """
    Read a text file.

    Args:
        file_path: Input file.

    Returns:
        List of non-empty lines.
    """

    path = Path(file_path)

    if not path.exists():
        return []

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


def write_file(file_path: str, data: list[str]) -> None:
    """
    Write a list to a text file.

    Args:
        file_path: Output file.
        data: List of strings.
    """

    path = Path(file_path)

    create_directory(path.parent)

    with path.open(
        "w",
        encoding="utf-8"
    ) as file:

        for item in data:
            file.write(f"{item}\n")


def timer(start_time: float) -> float:
    """
    Calculate elapsed time.

    Args:
        start_time: time.time()

    Returns:
        Elapsed seconds.
    """

    return round(
        time.time() - start_time,
        2
    )


def validate_domain(domain: str) -> bool:
    """
    Validate a domain name.

    Args:
        domain: Target domain.

    Returns:
        True if valid.
    """

    pattern = (
        r"^(?:[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}"
        r"[a-zA-Z0-9])?\.)+"
        r"[A-Za-z]{2,}$"
    )

    return bool(
        re.fullmatch(
            pattern,
            domain.strip()
        )
    )