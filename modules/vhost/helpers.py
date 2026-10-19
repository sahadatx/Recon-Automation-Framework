from pathlib import Path
from urllib.parse import urlparse

from config.config import VHOST_OUTPUT_DIR


def ensure_output_directory() -> Path:


    VHOST_OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return VHOST_OUTPUT_DIR


def normalize_target(
    target: str,
) -> str:


    target = target.strip()

    return target.rstrip("/")


def hostname(
    target: str,
) -> str:


    parsed = urlparse(normalize_target(target))

    return parsed.hostname or ""


def safe_filename(
    target: str,
) -> str:


    host = hostname(target)

    return host.replace(
        ".",
        "_",
    )


def build_host_header(
    target: str,
    host: str,
) -> str:


    domain = hostname(target)

    return f"{host}.{domain}"


def is_https(
    target: str,
) -> bool:


    return normalize_target(target).startswith("https://")


def is_http(
    target: str,
) -> bool:


    return normalize_target(target).startswith("http://")
