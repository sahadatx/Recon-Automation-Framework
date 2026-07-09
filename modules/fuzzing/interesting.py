"""
Directory Fuzzing Interesting Detection

Detects high-value files and directories
from directory fuzzing results.
"""

from pathlib import PurePosixPath


# ==========================================================
# Interesting Directories
# ==========================================================

INTERESTING_DIRECTORIES = {

    "admin",
    "administrator",
    "login",
    "dashboard",
    "panel",
    "cpanel",

    "api",
    "api/v1",
    "api/v2",

    "graphql",
    "graphiql",

    "swagger",
    "openapi",
    "docs",

    "debug",
    "dev",
    "staging",
    "sandbox",
    "internal",

    ".git",

    "uploads",
    "backup",

    "config",

}


# ==========================================================
# Interesting Files
# ==========================================================

INTERESTING_FILES = {

    ".env",
    ".env.local",
    ".env.production",

    "robots.txt",
    "security.txt",

    "config.php",
    "config.json",
    "config.yml",

    "settings.json",
    "settings.js",

    "package.json",
    "composer.json",

    "backup.zip",
    "backup.tar.gz",

    "db.sql",
    "database.sql",
    "dump.sql",

    "swagger.json",
    "swagger.yaml",
    "openapi.json",

    ".gitignore",
    ".git/config",

}


# ==========================================================
# Normalize Path
# ==========================================================

def normalize_path(
    url: str,
) -> str:
    """
    Normalize URL path.

    Returns:
        str
    """

    if not url:

        return ""

    if "://" in url:

        path = url.split(
            "://",
            1,
        )[1]

        path = path.split(
            "/",
            1,
        )

        if len(path) == 2:

            return path[1].strip("/")

        return ""

    return url.strip("/")


# ==========================================================
# Interesting File
# ==========================================================

def is_interesting_file(
    path: str,
) -> bool:
    """
    Check whether a file is interesting.

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
    Check whether a directory is interesting.

    Returns:
        bool
    """

    path = path.lower()

    parts = path.split("/")

    for directory in INTERESTING_DIRECTORIES:

        if (

            directory == path

            or

            directory in parts

            or

            path.startswith(
                directory + "/"
            )

        ):

            return True

    return False


# ==========================================================
# Detect Interesting Results
# ==========================================================

def detect_interesting(
    results: list,
):
    """
    Detect interesting paths.

    Args:
        results:
            Filtered ffuf results.

    Returns:
        dict
    """

    files = []

    directories = []

    for result in results:

        path = normalize_path(

            result.get(
                "url",
                "",
            )

        )

        if not path:

            continue

        if is_interesting_file(
            path
        ):

            files.append(
                result
            )

        if is_interesting_directory(
            path
        ):

            directories.append(
                result
            )

    statistics = {

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

    return {

        "files": files,

        "directories": directories,

        "statistics": statistics,

    }


# ==========================================================
# Entry Point
# ==========================================================

def scan(
    results: list,
):
    """
    Entry point.

    Args:
        results:
            Filtered ffuf results.

    Returns:
        dict
    """

    return detect_interesting(
        results
    )