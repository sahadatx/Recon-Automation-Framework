from pathlib import PurePosixPath


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


def normalize_path(
    url: str,
) -> str:


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


def is_interesting_file(
    path: str,
) -> bool:


    filename = PurePosixPath(path).name.lower()

    return filename in INTERESTING_FILES


def is_interesting_directory(
    path: str,
) -> bool:


    path = path.lower()

    parts = path.split("/")

    for directory in INTERESTING_DIRECTORIES:

        if directory == path or directory in parts or path.startswith(directory + "/"):

            return True

    return False


def detect_interesting(
    results: list,
):


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

        if is_interesting_file(path):

            files.append(result)

        if is_interesting_directory(path):

            directories.append(result)

    statistics = {
        "interesting_files": len(files),
        "interesting_directories": len(directories),
        "total": (len(files) + len(directories)),
    }

    return {
        "files": files,
        "directories": directories,
        "statistics": statistics,
    }


def scan(
    results: list,
):


    return detect_interesting(results)
