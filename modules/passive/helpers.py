"""
Passive Enumeration Helper Functions

Shared helper functions for passive reconnaissance modules.
"""

from __future__ import annotations

import re
import subprocess
import time

from collections.abc import (
    Callable,
    Mapping,
)
from functools import wraps
from typing import (
    Any,
    TypeVar,
)


from core.logger import (
    error,
    info,
    success,
    warning,
)

# ==========================================================
# Constants
# ==========================================================

DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}$")

IGNORED_KEYWORDS = frozenset(
    {
        "enumerating",
        "found",
        "api count exceeded",
        "increase quota",
        "error",
        "warning",
        "success",
        "info",
        "failed",
    }
)

IGNORED_PREFIXES = (
    "[",
    "+",
    "-",
    "*",
)


# ==========================================================
# Run External Command
# ==========================================================


def run_command(
    command: list[str],
    timeout: int = 60,
    env: Mapping[str, str] | None = None,
) -> list[str]:
    """
    Execute an external command.

    Args:
        command: Command and arguments.
        timeout: Maximum execution time in seconds.
        env: Optional environment variables.

    Returns:
        Command output as a list of non-empty lines.
    """

    try:

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=True,
            env=env,
        )

    except FileNotFoundError:

        error(f"{command[0]} is not installed.")

        return []

    except subprocess.TimeoutExpired:

        error(f"{command[0]} timed out.")

        return []

    except subprocess.CalledProcessError as exc:

        error(f"{command[0]} failed.")

        if exc.stdout:

            warning(exc.stdout.strip())

        if exc.stderr:

            error(exc.stderr.strip())

        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


# ==========================================================
# Normalize Subdomains
# ==========================================================


def normalize_subdomains(
    subdomains: list[str],
    domain: str,
) -> list[str]:
    """
    Normalize discovered subdomains.

    Processing steps:
        - Strip whitespace.
        - Convert to lowercase.
        - Remove wildcard prefix.
        - Remove tool banners.
        - Remove log messages.
        - Validate domain format.
        - Keep only the target domain.
        - Remove duplicates.
        - Return sorted results.

    Args:
        subdomains: Raw subdomains.
        domain: Target domain.

    Returns:
        Sorted normalized subdomains.
    """

    target_domain = domain.strip().lower()

    suffix = f".{target_domain}"

    cleaned: set[str] = set()

    for subdomain in subdomains:

        normalized = subdomain.strip().lower()

        if not normalized:
            continue

        if normalized.startswith("*."):

            normalized = normalized[2:]

        if normalized.startswith(IGNORED_PREFIXES):
            continue

        if any(keyword in normalized for keyword in IGNORED_KEYWORDS):
            continue

        if " " in normalized:
            continue

        if not DOMAIN_RE.fullmatch(normalized):
            continue

        if normalized != target_domain and not normalized.endswith(suffix):
            continue

        cleaned.add(normalized)

    return sorted(cleaned)


# ==========================================================
# Execute Enumeration Source
# ==========================================================


def execute_source(
    name: str,
    command: list[str],
    domain: str,
    timeout: int = 60,
    env: Mapping[str, str] | None = None,
) -> list[str]:
    """
    Execute a passive enumeration tool.

    Args:
        name: Tool name.
        command: Command and arguments.
        domain: Target domain.
        timeout: Maximum execution time in seconds.
        env: Optional environment variables.

    Returns:
        Normalized subdomains discovered by the tool.
    """

    info(f"Running {name}...")

    raw_results = run_command(
        command=command,
        timeout=timeout,
        env=env,
    )

    normalized_results = normalize_subdomains(
        raw_results,
        domain,
    )

    if normalized_results:

        success(f"{name} found " f"{len(normalized_results)} subdomains.")

    else:

        warning(f"{name} returned no results.")

    return normalized_results


# ==========================================================
# Retry Decorator
# ==========================================================

ReturnType = TypeVar(
    "ReturnType",
)


def retry_request(
    max_attempts: int = 3,
    delay: int = 2,
) -> Callable[
    [Callable[..., ReturnType]],
    Callable[..., ReturnType],
]:
    """
    Retry a function when it raises an exception.

    Args:
        max_attempts: Maximum retry attempts.
        delay: Delay between retries in seconds.

    Returns:
        Decorated function.
    """

    def decorator(
        function: Callable[..., ReturnType],
    ) -> Callable[..., ReturnType]:

        @wraps(function)
        def wrapper(
            *args: Any,
            **kwargs: Any,
        ) -> ReturnType:

            for attempt in range(
                1,
                max_attempts + 1,
            ):

                try:

                    return function(
                        *args,
                        **kwargs,
                    )

                except Exception as error:

                    if attempt == max_attempts:
                        raise

                    warning(
                        f"{function.__name__} failed "
                        f"(attempt {attempt}/{max_attempts}): "
                        f"{error}"
                    )

                    time.sleep(
                        delay,
                    )

            raise RuntimeError("Retry logic terminated unexpectedly.")

        return wrapper

    return decorator


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "run_command",
    "normalize_subdomains",
    "execute_source",
    "retry_request",
]
