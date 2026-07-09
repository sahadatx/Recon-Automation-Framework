"""
JavaScript Interesting Files Detection

Detects interesting files and directories
referenced inside JavaScript.
"""

from urllib.parse import (
    urlparse,
)

from pathlib import (
    PurePosixPath,
)


# ==========================================================
# Interesting Files
# ==========================================================

INTERESTING_FILES = {

    # Environment
    ".env",
    ".env.local",
    ".env.dev",
    ".env.test",
    ".env.production",

    # Config
    "config.js",
    "config.json",
    "config.php",
    "settings.js",
    "settings.json",
    "settings.yml",

    # API
    "swagger.json",
    "swagger.yaml",
    "swagger.yml",
    "openapi.json",
    "openapi.yaml",

    # Manifest
    "manifest.json",
    "asset-manifest.json",

    # Package
    "package.json",
    "package-lock.json",
    "composer.json",
    "composer.lock",
    "yarn.lock",

    # Build
    "webpack.config.js",
    "vite.config.js",

    # Firebase
    "firebase.json",
    "credentials.json",
    "service-account.json",
    "aws-exports.js",

    # Repository
    ".git",
    ".gitignore",
    ".git/config",
    ".svn",

    # Backup
    "backup.zip",
    "backup.tar",
    "backup.tar.gz",
    "backup.sql",
    "db.sql",
    "database.sql",
    "dump.sql",

    # Docker
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",

    # Robots
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

    parsed = urlparse(
        value
    )

    path = parsed.path

    path = str(
        PurePosixPath(
            path
        )
    )

    return path.strip(
        "/"
    )


# ==========================================================
# Interesting File
# ==========================================================

def is_interesting_file(
    path: str,
) -> bool:
    """
    Check interesting filename.

    Returns:
        bool
    """

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

    Returns:
        bool
    """

    path = path.lower()

    parts = path.split("/")

    for directory in INTERESTING_DIRECTORIES:

        if directory in path:

            return True

        if directory in parts:

            return True

    return False


# ==========================================================
# Detect Interesting Files
# ==========================================================

def detect_interesting_files(
    urls: list[str],
) -> list[str]:
    """
    Detect interesting files.

    Args:
        urls:
            Extracted URLs.

    Returns:
        list
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
) -> list[str]:
    """
    Detect interesting directories.

    Args:
        urls:
            Extracted URLs.

    Returns:
        list
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
# Generate Statistics
# ==========================================================

def generate_statistics(
    files: list[str],
    directories: list[str],
) -> dict:
    """
    Generate statistics.

    Returns:
        dict
    """

    return {

        "interesting_files": len(
            files
        ),

        "interesting_directories": len(
            directories
        ),

        "total": (

            len(files)

            +

            len(directories)

        ),

    }


# ==========================================================
# Scan
# ==========================================================

def scan(
    urls: list[str],
) -> dict:
    """
    Scan extracted URLs for
    interesting files and directories.

    Args:
        urls:
            URL list.

    Returns:
        dict
    """

    files = detect_interesting_files(
        urls
    )

    directories = detect_interesting_directories(
        urls
    )

    statistics = generate_statistics(

        files,

        directories,

    )

    return {

        "files": files,

        "directories": directories,

        "statistics": statistics,

    }


# ==========================================================
# Entry Point
# ==========================================================

def detect_interesting(
    urls: list[str],
) -> dict:
    """
    Entry point.

    Args:
        urls:
            URL list.

    Returns:
        dict
    """

    return scan(
        urls
    )


