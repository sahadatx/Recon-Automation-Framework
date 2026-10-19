import shutil
from pathlib import Path
from urllib.parse import urlparse


def is_nuclei_installed():


    return shutil.which("nuclei") is not None


def get_nuclei_version():


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


def ensure_directory(
    directory: str | Path,
):


    path = Path(directory)

    path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def cleanup_file(
    filepath: str | Path,
):


    path = Path(filepath)

    if not path.exists():

        return False

    try:

        path.unlink()

        return True

    except Exception:

        return False


def remove_duplicates(
    values: list,
):


    return list(dict.fromkeys(values))


def normalize_target(
    target: str,
):


    target = target.strip()

    if not target:

        return ""

    if not target.startswith(
        (
            "http://",
            "https://",
        )
    ):

        target = "https://" + target

    parsed = urlparse(target)

    scheme = parsed.scheme

    host = parsed.netloc.lower()

    return f"{scheme}://{host}"


def normalize_targets(
    targets: list[str],
):


    normalized = [normalize_target(target) for target in targets if target.strip()]

    return remove_duplicates(normalized)


def validate_target(
    target: str,
):


    target = normalize_target(target)

    if not target:

        return False

    parsed = urlparse(target)

    return bool(parsed.scheme and parsed.netloc)


def validate_targets(
    targets: list[str],
):


    return [target for target in normalize_targets(targets) if validate_target(target)]


def read_lines(
    filepath: str | Path,
):


    path = Path(filepath)

    if not path.exists():

        return []

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            return [line.strip() for line in file if line.strip()]

    except Exception:

        return []


def write_lines(
    filepath: str | Path,
    lines: list[str],
):


    path = Path(filepath)

    ensure_directory(path.parent)

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:

        for line in lines:

            file.write(line + "\n")

    return path


def load_targets(
    filepath: str | Path,
):


    targets = read_lines(filepath)

    return validate_targets(targets)


def save_targets(
    filepath: str | Path,
    targets: list[str],
):


    targets = validate_targets(targets)

    return write_lines(
        filepath,
        targets,
    )


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

    normalized = normalize_targets(sample)

    print(
        "Normalized:",
        normalized,
    )

    print(
        "Valid:",
        validate_targets(sample),
    )
