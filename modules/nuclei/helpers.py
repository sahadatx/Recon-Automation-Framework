"""
Nuclei Helpers

Shared helper functions for
the Nuclei module.
"""

import shutil

from pathlib import Path

from urllib.parse import urlparse


# ==========================================================
# Check Installation
# ==========================================================

def is_nuclei_installed():
    """
    Check whether Nuclei is
    installed.

    Returns:
        bool
    """

    return (

        shutil.which(
            "nuclei"
        )

        is not None

    )


# ==========================================================
# Get Version
# ==========================================================

def get_nuclei_version():
    """
    Return installed Nuclei
    version.

    Returns:
        str | None
    """

    import subprocess

    try:

        result = subprocess.run(

            [

                "nuclei",

                "-version",

            ],

            capture_output=True,

            text=True,

            timeout=5,

        )

        return result.stdout.strip()

    except Exception:

        return None


# ==========================================================
# Ensure Directory
# ==========================================================

def ensure_directory(
    directory: str | Path,
):
    """
    Create directory if it
    does not exist.

    Returns:
        Path
    """

    path = Path(
        directory
    )

    path.mkdir(

        parents=True,

        exist_ok=True,

    )

    return path


# ==========================================================
# Cleanup File
# ==========================================================

def cleanup_file(
    filepath: str | Path,
):
    """
    Delete file safely.

    Returns:
        bool
    """

    path = Path(
        filepath
    )

    if not path.exists():

        return False

    try:

        path.unlink()

        return True

    except Exception:

        return False


# ==========================================================
# Remove Duplicates
# ==========================================================

def remove_duplicates(
    values: list,
):
    """
    Remove duplicate values
    while preserving order.

    Returns:
        list
    """

    return list(

        dict.fromkeys(
            values
        )

    )


# ==========================================================
# Normalize Target
# ==========================================================

def normalize_target(
    target: str,
):
    """
    Normalize one target.

    Returns:
        str
    """

    target = target.strip()

    if not target:

        return ""

    if not target.startswith(

        (

            "http://",

            "https://",

        )

    ):

        target = (

            "https://"

            + target

        )

    parsed = urlparse(
        target
    )

    scheme = parsed.scheme

    host = parsed.netloc.lower()

    return (

        f"{scheme}://{host}"

    )


# ==========================================================
# Normalize Targets
# ==========================================================

def normalize_targets(
    targets: list[str],
):
    """
    Normalize target list.

    Returns:
        list
    """

    normalized = [

        normalize_target(
            target
        )

        for target in targets

        if target.strip()

    ]

    return remove_duplicates(
        normalized
    )


# ==========================================================
# Validate Target
# ==========================================================

def validate_target(
    target: str,
):
    """
    Validate one target.

    Returns:
        bool
    """

    target = normalize_target(
        target
    )

    if not target:

        return False

    parsed = urlparse(
        target
    )

    return bool(

        parsed.scheme

        and parsed.netloc

    )


# ==========================================================
# Validate Targets
# ==========================================================

def validate_targets(
    targets: list[str],
):
    """
    Validate target list.

    Returns:
        list
    """

    return [

        target

        for target in normalize_targets(
            targets
        )

        if validate_target(
            target
        )

    ]


# ==========================================================
# Read Lines
# ==========================================================

def read_lines(
    filepath: str | Path,
):
    """
    Read file lines.

    Returns:
        list
    """

    path = Path(
        filepath
    )

    if not path.exists():

        return []

    try:

        with path.open(

            "r",

            encoding="utf-8",

        ) as file:

            return [

                line.strip()

                for line in file

                if line.strip()

            ]

    except Exception:

        return []


# ==========================================================
# Write Lines
# ==========================================================

def write_lines(
    filepath: str | Path,
    lines: list[str],
):
    """
    Write file lines.

    Returns:
        Path
    """

    path = Path(
        filepath
    )

    ensure_directory(
        path.parent
    )

    with path.open(

        "w",

        encoding="utf-8",

    ) as file:

        for line in lines:

            file.write(
                line + "\n"
            )

    return path


# ==========================================================
# Load Targets
# ==========================================================

def load_targets(
    filepath: str | Path,
):
    """
    Load targets from file.

    Returns:
        list
    """

    targets = read_lines(
        filepath
    )

    return validate_targets(
        targets
    )


# ==========================================================
# Save Targets
# ==========================================================

def save_targets(
    filepath: str | Path,
    targets: list[str],
):
    """
    Save normalized targets.

    Returns:
        Path
    """

    targets = validate_targets(
        targets
    )

    return write_lines(

        filepath,

        targets,

    )


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    print(
        "Installed:",
        is_nuclei_installed(),
    )

    print(
        "Version:",
        get_nuclei_version(),
    )

    sample = [

        "example.com",

        "https://example.com",

        "http://testphp.vulnweb.com",

        "example.com",

    ]

    normalized = normalize_targets(
        sample
    )

    print(
        "Normalized:",
        normalized,
    )

    print(
        "Valid:",
        validate_targets(
            sample
        ),
    )