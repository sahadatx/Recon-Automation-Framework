"""
Directory Fuzzing Scanner

Builds and executes ffuf
commands against target URLs.
"""

import subprocess
import tempfile

from pathlib import Path

from config.config import (

    FUZZ_THREADS,

    FUZZ_TIMEOUT,

    FUZZ_RATE_LIMIT,

    FUZZ_MATCH_CODES,

    FUZZ_FILTER_CODES,

    FUZZ_DEFAULT_WORDLIST,

    HTTP_USER_AGENT,

    FUZZ_AUTO_CALIBRATION,
    

)

from core.logger import (

    info,

    warning,

)


# ==========================================================
# Validate Target
# ==========================================================

def validate_target(
    target: str,
) -> bool:
    """
    Validate target URL.

    Args:
        target:
            Target URL.

    Returns:
        bool
    """

    return (

        bool(target)

        and

        target.startswith(

            (

                "http://",

                "https://",

            )

        )

    )


# ==========================================================
# Build ffuf Command
# ==========================================================

def build_command(
    target: str,
    wordlist: Path | str | None = None,
    threads: int = FUZZ_THREADS,
    timeout: int = FUZZ_TIMEOUT,
    match_codes: str = FUZZ_MATCH_CODES,
    filter_codes: str = FUZZ_FILTER_CODES,
) -> tuple[list[str], Path]:
    """
    Build ffuf command.

    Args:
        target:
            Target URL.

        wordlist:
            Custom wordlist.

        threads:
            Worker threads.

        timeout:
            Maximum runtime.

        match_codes:
            HTTP status codes
            to match.

        filter_codes:
            HTTP status codes
            to filter.

    Returns:
        tuple
    """

    if not validate_target(
        target
    ):

        raise ValueError(

            f"Invalid target: {target}"

        )

    if threads < 1:

        raise ValueError(

            "Thread count must be greater than zero."

        )

    if timeout < 1:

        raise ValueError(

            "Timeout must be greater than zero."

        )

    target = target.rstrip("/")

    if wordlist is None:

        wordlist = (

            FUZZ_DEFAULT_WORDLIST

        )

    else:

        wordlist = Path(

            wordlist

        )

    if (

        not wordlist.exists()

        or

        not wordlist.is_file()

    ):

        raise FileNotFoundError(

            f"Wordlist not found: {wordlist}"

        )

    output_file = Path(

        tempfile.mkstemp(

            suffix=".json",

        )[1]

    )

    command = [

        "ffuf",

        "-u",

        f"{target}/FUZZ",

        "-w",

        str(wordlist),

        "-H",

        f"User-Agent: {HTTP_USER_AGENT}",

        "-t",

        str(threads),

        "-maxtime",

        str(timeout),

        "-rate",

        str(FUZZ_RATE_LIMIT),

        "-mc",

        match_codes,

        "-fc",

        filter_codes,

        "-of",

        "json",

        "-o",

        str(output_file),

    ]

    return (

        command,

        output_file,

    )


# ==========================================================
# Run ffuf
# ==========================================================

def run_ffuf(
    target: str,
    wordlist: Path | str | None = None,
    threads: int = FUZZ_THREADS,
    timeout: int = FUZZ_TIMEOUT,
    match_codes: str = FUZZ_MATCH_CODES,
    filter_codes: str = FUZZ_FILTER_CODES,
) -> tuple[Path | None, str | None]:
    """
    Execute ffuf.

    Returns:
        tuple
    """

    command, output_file = build_command(

        target=target,

        wordlist=wordlist,

        threads=threads,

        timeout=timeout,

        match_codes=match_codes,

        filter_codes=filter_codes,

    )

    info(

        f"Running ffuf against {target}"

    )

    try:

        subprocess.run(

            command,

            stdout=subprocess.DEVNULL,

            stderr=subprocess.PIPE,

            text=True,

            timeout=timeout,

            check=True,

        )

        return (

            output_file,

            None,

        )

    except subprocess.CalledProcessError as error:

        warning(

            f"ffuf failed: {target}"

        )

        return (

            None,

            error.stderr.strip(),

        )

    except subprocess.TimeoutExpired:

        warning(

            f"ffuf timeout: {target}"

        )

        return (

            None,

            f"Timeout ({timeout}s)",

        )

    except FileNotFoundError:

        warning(

            "ffuf is not installed."

        )

        return (

            None,

            "ffuf not installed",

        )


# ==========================================================
# Scan Target
# ==========================================================

def scan_target(
    target: str,
    wordlist: Path | str | None = None,
) -> dict:
    """
    Scan one target.

    Returns:
        dict
    """

    output_file, error = run_ffuf(

        target=target,

        wordlist=wordlist,

    )

    return {

        "target": target,

        "success": error is None,

        "output": output_file,

        "error": error,

    }


# ==========================================================
# Cleanup
# ==========================================================

def cleanup(
    output_file: Path | None,
) -> None:
    """
    Remove temporary
    output file.

    Returns:
        None
    """

    if output_file is None:

        return

    try:

        output_file.unlink(

            missing_ok=True,

        )

    except Exception:

        pass


# ==========================================================
# Check ffuf Installation
# ==========================================================

def is_ffuf_installed() -> bool:
    """
    Check whether ffuf
    is installed.

    Returns:
        bool
    """

    try:

        subprocess.run(

            [

                "ffuf",

                "-V",

            ],

            stdout=subprocess.DEVNULL,

            stderr=subprocess.DEVNULL,

            check=True,

        )

        return True

    except Exception:

        return False


# ==========================================================
# ffuf Version
# ==========================================================

def get_ffuf_version() -> str:
    """
    Return installed
    ffuf version.

    Returns:
        str
    """

    try:

        result = subprocess.run(

            [

                "ffuf",

                "-V",

            ],

            capture_output=True,

            text=True,

            check=True,

        )

        return result.stdout.strip()

    except Exception:

        return "Unknown"


# ==========================================================
# JSON Support
# ==========================================================

def supports_json() -> bool:
    """
    Check whether ffuf
    supports JSON output.

    Returns:
        bool
    """

    return True


# ==========================================================
# Recursion Support
# ==========================================================

def supports_recursion() -> bool:
    """
    Check whether ffuf
    supports recursion.

    Returns:
        bool
    """

    return True


# ==========================================================
# Auto Calibration Support
# ==========================================================

def supports_auto_calibration() -> bool:
    """
    Check whether ffuf
    supports auto calibration.

    Returns:
        bool
    """

    return True
