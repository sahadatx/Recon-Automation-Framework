"""
Passive Enumeration Helper Functions

Shared helper functions for passive reconnaissance modules.
"""

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

        error(f"{command[0]} is not installed.")

    except subprocess.TimeoutExpired:

        error(f"{command[0]} timed out.")

    except subprocess.CalledProcessError as e:

        error(f"{command[0]} failed.")

        if e.stderr:
            error(e.stderr.strip())

    return []


# ==========================================================
# Normalize Subdomains
# ==========================================================

def normalize_subdomains(
    subdomains: list[str],
) -> list[str]:
    """
    Normalize discovered subdomains.

    - Strip whitespace
    - Convert to lowercase
    - Remove wildcard (*.)
    - Remove duplicates
    - Sort alphabetically
    """

    cleaned = set()

    for subdomain in subdomains:

        subdomain = subdomain.strip().lower()

        if not subdomain:
            continue

        if subdomain.startswith("*."):
            subdomain = subdomain[2:]

        cleaned.add(subdomain)

    return sorted(cleaned)


# ==========================================================
# Execute Enumeration Source
# ==========================================================

def execute_source(
    name: str,
    command: list[str],
    timeout: int = 60,
    env: dict | None = None,
) -> list[str]:
    """
    Execute a passive enumeration source.

    Args:
        name: Tool name.
        command: Command to execute.
        timeout: Command timeout.
        env: Optional environment variables.

    Returns:
        Normalized subdomain list.
    """

    info(f"Running {name}...")

    results = normalize_subdomains(
        run_command(
            command=command,
            timeout=timeout,
            env=env,
        )
    )

    if results:

        success(
            f"{name} found {len(results)} subdomains."
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

            for attempt in range(max_attempts):

                try:

                    return function(
                        *args,
                        **kwargs
                    )

                except Exception:

                    if attempt == max_attempts - 1:
                        raise

                    warning(
                        f"Retry {attempt + 1}/{max_attempts}"
                    )

                    time.sleep(delay)

        return wrapper

    return decorator