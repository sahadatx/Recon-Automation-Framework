"""
Directory Fuzzing Wordlists

Manages built-in and custom wordlists.
"""

from pathlib import Path


# ==========================================================
# Wordlist Directory
# ==========================================================

WORDLIST_DIRECTORY = (

    Path(__file__).parent

    / "wordlists"

)


# ==========================================================
# Default Wordlists
# ==========================================================

COMMON = (

    WORDLIST_DIRECTORY

    / "common.txt"

)

SMALL = (

    WORDLIST_DIRECTORY

    / "small.txt"

)

MEDIUM = (

    WORDLIST_DIRECTORY

    / "medium.txt"

)

LARGE = (

    WORDLIST_DIRECTORY

    / "large.txt"

)


# ==========================================================
# Specialized Wordlists
# ==========================================================

ADMIN = (

    WORDLIST_DIRECTORY

    / "admin.txt"

)

API = (

    WORDLIST_DIRECTORY

    / "api.txt"

)

BACKUP = (

    WORDLIST_DIRECTORY

    / "backup.txt"

)

FILES = (

    WORDLIST_DIRECTORY

    / "files.txt"

)

# ==========================================================
# Available Wordlists
# ==========================================================

AVAILABLE_WORDLISTS = {

    "common": COMMON,

    "small": SMALL,

    "medium": MEDIUM,

    "large": LARGE,

    "admin": ADMIN,

    "api": API,

    "backup": BACKUP,

    "files": FILES,

}


# ==========================================================
# Validate Wordlist
# ==========================================================

def validate_wordlist(
    path: Path,
) -> bool:
    """
    Validate a wordlist.

    Args:
        path:
            Wordlist path.

    Returns:
        bool
    """

    return (

        path.exists()

        and

        path.is_file()

    )


# ==========================================================
# Get Wordlist
# ==========================================================

def get_wordlist(
    name: str = "common",
    custom: str | None = None,
) -> Path:
    """
    Get a built-in or custom wordlist.

    Args:
        name:
            Built-in wordlist name.

        custom:
            Custom wordlist path.

    Returns:
        Path
    """

    # ------------------------------------------------------
    # Custom Wordlist
    # ------------------------------------------------------

    if custom:

        path = Path(
            custom
        )

        if validate_wordlist(
            path
        ):

            return path

        raise FileNotFoundError(

            f"Wordlist not found: {path}"

        )

    # ------------------------------------------------------
    # Built-in Wordlist
    # ------------------------------------------------------

    path = AVAILABLE_WORDLISTS.get(

        name.lower(),

        COMMON,

    )

    if not validate_wordlist(
        path
    ):

        raise FileNotFoundError(

            f"Wordlist not found: {path}"

        )

    return path