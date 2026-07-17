"""
Virtual Host Discovery Helpers

Shared helper functions used by the
Virtual Host Discovery module.
"""

from pathlib import Path

from urllib.parse import (
    urlparse,
)

from config.config import (

    VHOST_OUTPUT_DIR,

)


# ==========================================================
# Output Directory
# ==========================================================

def ensure_output_directory() -> Path:
    """
    Create output directory.

    Returns:
        Path
    """

    VHOST_OUTPUT_DIR.mkdir(

        parents=True,

        exist_ok=True,

    )

    return VHOST_OUTPUT_DIR


# ==========================================================
# Normalize Target
# ==========================================================

def normalize_target(
    target: str,
) -> str:
    """
    Normalize target URL.

    Returns:
        str
    """

    target = target.strip()

    return target.rstrip("/")


# ==========================================================
# Extract Hostname
# ==========================================================

def hostname(
    target: str,
) -> str:
    """
    Return hostname.

    Returns:
        str
    """

    parsed = urlparse(

        normalize_target(

            target

        )

    )

    return parsed.hostname or ""


# ==========================================================
# Safe Filename
# ==========================================================

def safe_filename(
    target: str,
) -> str:
    """
    Convert target into
    filesystem-safe filename.

    Returns:
        str
    """

    host = hostname(
        target
    )

    return (

        host

        .replace(

            ".",

            "_",

        )

    )


# ==========================================================
# Build Host Header
# ==========================================================

def build_host_header(
    target: str,
    host: str,
) -> str:
    """
    Build virtual host header.

    Args:
        target:
            Target URL.

        host:
            Virtual host.

    Returns:
        str
    """

    domain = hostname(
        target
    )

    return f"{host}.{domain}"


# ==========================================================
# Is HTTPS
# ==========================================================

def is_https(
    target: str,
) -> bool:
    """
    Check HTTPS target.

    Returns:
        bool
    """

    return normalize_target(

        target

    ).startswith(

        "https://"

    )


# ==========================================================
# Is HTTP
# ==========================================================

def is_http(
    target: str,
) -> bool:
    """
    Check HTTP target.

    Returns:
        bool
    """

    return normalize_target(

        target

    ).startswith(

        "http://"

    )