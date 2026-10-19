import subprocess
import tempfile
from pathlib import Path

from config.config import NUCLEI_RATE_LIMIT, NUCLEI_THREADS, NUCLEI_TIMEOUT
from modules.nuclei.templates import get_templates


DEFAULT_SEVERITY = "critical,high,medium,low,info"

DEFAULT_RETRIES = 2

DEFAULT_JSONL = True


def validate_target(
    target: str,
) -> bool:


    return isinstance(
        target,
        str,
    ) and target.startswith(
        (
            "http://",
            "https://",
        )
    )


def build_command(
    output_file: Path,
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
):


    command = [
        "nuclei",
        "-jsonl",
        "-o",
        str(output_file),
        "-severity",
        severity,
        "-rate-limit",
        str(NUCLEI_RATE_LIMIT),
        "-c",
        str(NUCLEI_THREADS),
    ]

    templates = get_templates(
        profile=profile,
        custom=custom_template,
    )

    for template in templates:

        command.extend(
            [
                "-t",
                str(template),
            ]
        )

    return command


def create_output_file():


    return Path(
        tempfile.mkstemp(
            suffix=".jsonl",
        )[1]
    )


def build_single_target(
    target: str,
    output_file: Path,
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
):


    command = build_command(
        output_file,
        profile,
        custom_template,
        severity,
    )

    command.extend(
        [
            "-target",
            target,
        ]
    )

    return command


def build_multiple_targets(
    target_file: Path,
    output_file: Path,
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
):


    command = build_command(
        output_file,
        profile,
        custom_template,
        severity,
    )

    command.extend(
        [
            "-list",
            str(target_file),
        ]
    )

    return command


def run_single_target(
    target: str,
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
    retries: int = DEFAULT_RETRIES,
):


    if not validate_target(target):

        return (
            None,
            "Invalid target",
        )

    output_file = create_output_file()

    command = build_single_target(
        target,
        output_file,
        profile,
        custom_template,
        severity,
    )

    last_error = None

    for _ in range(retries + 1):

        try:

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                timeout=NUCLEI_TIMEOUT,
                check=True,
            )

            return (
                output_file,
                None,
            )

        except subprocess.TimeoutExpired:

            last_error = f"Timeout ({NUCLEI_TIMEOUT}s)"

        except subprocess.CalledProcessError as error:

            last_error = error.stderr.strip()

        except Exception as error:

            last_error = str(error)

    cleanup(output_file)

    return (
        None,
        last_error,
    )


def run_multiple_targets(
    targets: list[str],
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
    retries: int = DEFAULT_RETRIES,
):


    if not targets:

        return (
            None,
            "No targets",
        )

    output_file = create_output_file()

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False,
        encoding="utf-8",
    ) as file:

        for target in targets:

            file.write(target + "\n")

        target_file = Path(file.name)

    command = build_multiple_targets(
        target_file,
        output_file,
        profile,
        custom_template,
        severity,
    )

    last_error = None

    for _ in range(retries + 1):

        try:

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                timeout=NUCLEI_TIMEOUT,
                check=True,
            )

            cleanup(target_file)

            return (
                output_file,
                None,
            )

        except subprocess.TimeoutExpired:

            last_error = f"Timeout ({NUCLEI_TIMEOUT}s)"

        except subprocess.CalledProcessError as error:

            last_error = error.stderr.strip()

        except Exception as error:

            last_error = str(error)

    cleanup(target_file)

    cleanup(output_file)

    return (
        None,
        last_error,
    )


def cleanup(
    filepath,
):


    if not filepath:

        return

    try:

        Path(filepath).unlink(
            missing_ok=True,
        )

    except Exception:

        pass


def is_nuclei_installed():


    try:

        subprocess.run(
            [
                "nuclei",
                "-version",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )

        return True

    except Exception:

        return False


def get_nuclei_version():


    try:

        result = subprocess.run(
            [
                "nuclei",
                "-version",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except Exception:

        return "Unknown"


def scan_target(
    target: str,
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
):


    output, error = run_single_target(
        target,
        profile,
        custom_template,
        severity,
    )

    return {
        "success": error is None,
        "output": output,
        "error": error,
    }


def scan_targets(
    targets: list[str],
    profile: str = "default",
    custom_template: str | None = None,
    severity: str = DEFAULT_SEVERITY,
):


    output, error = run_multiple_targets(
        targets,
        profile,
        custom_template,
        severity,
    )

    return {
        "success": error is None,
        "output": output,
        "error": error,
    }


def supports_multiple_targets():

    return True


def supports_jsonl():

    return DEFAULT_JSONL


if __name__ == "__main__":

    print(
        "Installed :",
        is_nuclei_installed(),
    )

    print(
        "Version   :",
        get_nuclei_version(),
    )
