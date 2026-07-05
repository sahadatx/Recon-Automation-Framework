"""
Passive Enumeration Helper Functions

Shared helper functions for passive reconnaissance modules.
"""

import subprocess
import time
from functools import wraps


# ==========================================================
# Run External Command
# ==========================================================

def run_command(command, timeout=60):
    """
    Execute a shell command and return its output.

    Args:
        command (list): Command to execute.
        timeout (int): Timeout in seconds.

    Returns:
        list[str]
    """

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )

        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    except FileNotFoundError:

        return []

    except subprocess.TimeoutExpired:

        return []

    except subprocess.CalledProcessError:

        return []


# ==========================================================
# Normalize Subdomains
# ==========================================================

def normalize_subdomains(subdomains):
    """
    Normalize discovered subdomains.

    - lowercase
    - remove whitespace
    - remove wildcard
    - remove duplicates
    - sort alphabetically
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

def execute_source(name, command, timeout=60):
    """
    Execute a passive enumeration tool.

    Args:
        name (str): Tool name.
        command (list): Command.

    Returns:
        list[str]
    """

    from core.logger import (
        info,
        success,
        warning,
    )

    info(f"Running {name}...")

    results = normalize_subdomains(
        run_command(
            command,
            timeout=timeout
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

def retry_request(max_attempts=3, delay=2):
    """
    Retry decorator.

    Args:
        max_attempts (int)
        delay (int)
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

                    time.sleep(delay)

        return wrapper

    return decorator