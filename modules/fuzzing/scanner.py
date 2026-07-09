"""
Directory Fuzzing Scanner

Runs ffuf against target URLs.
"""

import subprocess
import tempfile

from pathlib import Path

from config.config import (
    FUZZ_THREADS,
    FUZZ_TIMEOUT,
    FUZZ_MATCH_CODES,
)

from core.logger import (
    info,
    warning,
)

from modules.fuzzing.wordlists import (
    get_wordlist,
)


# ==========================================================
# Build ffuf Command
# ==========================================================

def build_command(
    target: str,
    wordlist: str = "common",
    custom_wordlist: str | None = None,
    threads: int = FUZZ_THREADS,
    timeout: int = FUZZ_TIMEOUT,
    match_codes: str = FUZZ_MATCH_CODES,
) -> tuple[list[str], Path]:
    """
    Build ffuf command.
    """

    target = target.rstrip("/")

    wordlist_path = get_wordlist(

        name=wordlist,

        custom=custom_wordlist,

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

        str(wordlist_path),

        "-t",

        str(threads),

        "-maxtime",

        str(timeout),

        "-mc",

        match_codes,

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
    wordlist: str = "common",
    custom_wordlist: str | None = None,
    threads: int = FUZZ_THREADS,
    timeout: int = FUZZ_TIMEOUT,
    match_codes: str = FUZZ_MATCH_CODES,
):
    """
    Execute ffuf.
    """

    command, output_file = build_command(

        target=target,

        wordlist=wordlist,

        custom_wordlist=custom_wordlist,

        threads=threads,

        timeout=timeout,

        match_codes=match_codes,

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

            "Timeout",

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
    wordlist: str = "common",
    custom_wordlist: str | None = None,
):
    """
    Scan one target.

    Returns:
        dict
    """

    output_file, error = run_ffuf(

        target=target,

        wordlist=wordlist,

        custom_wordlist=custom_wordlist,

    )

    if error:

        return {

            "target": target,

            "success": False,

            "output": None,

            "error": error,

        }

    return {

        "target": target,

        "success": True,

        "output": output_file,

        "error": None,

    }


# ==========================================================
# Cleanup
# ==========================================================

def cleanup(
    output_file: Path | None,
):
    """
    Remove temporary ffuf output.
    """

    if not output_file:

        return

    try:

        output_file.unlink(
            missing_ok=True,
        )

    except Exception:

        pass