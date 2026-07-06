"""
Passive Enumeration Helper Functions

Shared helper functions for passive reconnaissance modules.
"""

import re
import subprocess
import time
from functools import wraps

from core.logger import (
    info,
    success,
    warning,
    error,
)


# ==========================================================
# Run External Command
# ==========================================================

def run_command(
    command: list[str],
    timeout: int = 60,
    env: dict | None = None,
) -> list[str]:
    """
    Execute an external command.

    Args:
        command: Command to execute.
        timeout: Timeout in seconds.
        env: Optional environment variables.

    Returns:
        List of command output lines.
    """

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True,
            env=env,
        )

        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    except FileNotFoundError:

        error(
            f"{command[0]} is not installed."
        )

    except subprocess.TimeoutExpired:

        error(
            f"{command[0]} timed out."
        )

    except subprocess.CalledProcessError as exc:

        error(
            f"{command[0]} failed."
        )

        if exc.stderr:

            error(
                exc.stderr.strip()
            )

    return []


# ==========================================================
# Normalize Subdomains
# ==========================================================

def normalize_subdomains(
    subdomains: list[str],
    domain: str,
) -> list[str]:
    """
    Normalize discovered subdomains.

    - Strip whitespace
    - Convert to lowercase
    - Remove wildcard (*.)
    - Keep only target domain
    - Remove tool banners
    - Remove API messages
    - Remove invalid entries
    - Remove duplicates
    - Sort alphabetically
    """

    cleaned = set()

    domain = domain.lower().strip()

    domain_pattern = re.compile(
        r"^(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}$"
    )

    ignored_keywords = (
        "enumerating",
        "found",
        "api count exceeded",
        "increase quota",
        "error",
        "warning",
        "success",
        "info",
        "failed",
    )

    ignored_prefixes = (
        "[",
        "+",
        "-",
        "*",
    )

    for subdomain in subdomains:

        subdomain = (
            subdomain
            .strip()
            .lower()
        )

        if not subdomain:
            continue

        # Remove wildcard
        if subdomain.startswith("*."):

            subdomain = subdomain[2:]

        # Skip tool banners
        if subdomain.startswith(
            ignored_prefixes
        ):
            continue

        # Skip log messages
        if any(
            keyword in subdomain
            for keyword in ignored_keywords
        ):
            continue

        # Skip entries with spaces
        if " " in subdomain:
            continue

        # Validate domain format
        if not domain_pattern.fullmatch(
            subdomain
        ):
            continue

        # Keep only target domain
        if (
            subdomain != domain
            and not subdomain.endswith(
                "." + domain
            )
        ):
            continue

        cleaned.add(
            subdomain
        )

    return sorted(
        cleaned
    )


# ==========================================================
# Execute Enumeration Source
# ==========================================================

def execute_source(
    name: str,
    command: list[str],
    domain: str,
    timeout: int = 60,
    env: dict | None = None,
) -> list[str]:
    """
    Execute a passive enumeration source.

    Args:
        name: Tool name.
        command: Command to execute.
        domain: Target domain.
        timeout: Command timeout.
        env: Optional environment variables.

    Returns:
        Normalized subdomain list.
    """

    info(
        f"Running {name}..."
    )

    raw_results = run_command(
        command=command,
        timeout=timeout,
        env=env,
    )

    results = normalize_subdomains(
        raw_results,
        domain,
    )

    if results:

        success(
            f"{name} found "
            f"{len(results)} subdomains."
        )

    else:

        warning(
            f"{name} returned no results."
        )

    return results


# ==========================================================
# Retry Decorator
# ==========================================================

def retry_request(
    max_attempts: int = 3,
    delay: int = 2,
):
    """
    Retry decorator for network requests.
    """

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            for attempt in range(
                max_attempts
            ):

                try:

                    return function(
                        *args,
                        **kwargs,
                    )

                except Exception:

                    if attempt == max_attempts - 1:

                        raise

                    warning(
                        f"Retry "
                        f"{attempt + 1}/"
                        f"{max_attempts}"
                    )

                    time.sleep(
                        delay
                    )

        return wrapper

    return decorator