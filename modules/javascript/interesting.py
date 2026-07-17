"""
JavaScript Interesting Files Detection

Detects interesting files and directories
referenced inside JavaScript.
"""

from pathlib import PurePosixPath
from urllib.parse import urlparse

from core.logger import (
    debug,
)


# ==========================================================
# Interesting Files
# ==========================================================

INTERESTING_FILES = {

    ".env",
    ".env.local",
    ".env.dev",
    ".env.test",
    ".env.production",

    "config.js",
    "config.json",
    "config.php",
    "settings.js",
    "settings.json",
    "settings.yml",

    "swagger.json",
    "swagger.yaml",
    "swagger.yml",
    "openapi.json",
    "openapi.yaml",

    "manifest.json",
    "asset-manifest.json",

    "package.json",
    "package-lock.json",
    "composer.json",
    "composer.lock",
    "yarn.lock",

    "webpack.config.js",
    "vite.config.js",

    "firebase.json",
    "credentials.json",
    "service-account.json",
    "aws-exports.js",

    ".git",
    ".gitignore",
    ".git/config",
    ".svn",

    "backup.zip",
    "backup.tar",
    "backup.tar.gz",
    "backup.sql",
    "db.sql",
    "database.sql",
    "dump.sql",

    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",

    "robots.txt",
    "security.txt",

}


# ==========================================================
# Interesting Directories
# ==========================================================

INTERESTING_DIRECTORIES = {

    "api",
    "api/v1",
    "api/v2",

    "admin",

    "dashboard",

    "graphql",
    "graphiql",

    "internal",

    "uploads",

    "backup",

    "config",

    "debug",

    "dev",

    "staging",

    "sandbox",

    "docs",

    "swagger",

    "test",

    "tests",

}


# ==========================================================
# Normalize Path
# ==========================================================

def normalize(
    value: str,
) -> str:
    """
    Normalize URL path.

    Returns:
        str
    """

    if not value:

        return ""

    try:

        parsed = urlparse(

            value

        )

    except ValueError as error:

        debug(

            f"Skipping invalid URL: {value} ({error})"

        )

        return ""

    try:

        path = str(

            PurePosixPath(

                parsed.path

            )

        )

    except Exception:

        return ""

    return path.strip("/")


# ==========================================================
# Interesting File
# ==========================================================

def is_interesting_file(
    path: str,
) -> bool:
    """
    Check interesting filename.
    """

    if not path:

        return False

    filename = PurePosixPath(

        path

    ).name.lower()

    return (

        filename

        in

        INTERESTING_FILES

    )


# ==========================================================
# Interesting Directory
# ==========================================================

def is_interesting_directory(
    path: str,
) -> bool:
    """
    Check interesting directory.
    """

    if not path:

        return False

    path = path.lower()

    parts = path.split("/")

    return any(

        directory in path

        or

        directory in parts

        for directory

        in INTERESTING_DIRECTORIES

    )


# ==========================================================
# Detect Interesting Files
# ==========================================================

def detect_interesting_files(
    urls: list[str],
):
    """
    Detect interesting files.
    """

    findings = set()

    for url in urls:

        path = normalize(

            url

        )

        if not path:

            continue

        if is_interesting_file(

            path

        ):

            findings.add(

                path

            )

    return sorted(

        findings

    )


# ==========================================================
# Detect Interesting Directories
# ==========================================================

def detect_interesting_directories(
    urls: list[str],
):
    """
    Detect interesting directories.
    """

    findings = set()

    for url in urls:

        path = normalize(

            url

        )

        if not path:

            continue

        if is_interesting_directory(

            path

        ):

            findings.add(

                path

            )

    return sorted(

        findings

    )


# ==========================================================
# Statistics
# ==========================================================

def generate_statistics(
    files,
    directories,
):
    """
    Generate statistics.
    """

    return {

        "interesting_files": len(

            files

        ),

        "interesting_directories": len(

            directories

        ),

        "total": len(

            files

        ) + len(

            directories

        ),

    }


# ==========================================================
# Scan
# ==========================================================

def scan(
    urls,
):
    """
    Scan interesting files
    and directories.
    """

    files = detect_interesting_files(

        urls

    )

    directories = detect_interesting_directories(

        urls

    )

    return {

        "files": files,

        "directories": directories,

        "statistics": generate_statistics(

            files,

            directories,

        ),

    }


# ==========================================================
# Entry Point
# ==========================================================

def detect_interesting(
    urls,
):
    """
    Entry point.
    """

    return scan(

        urls

    )