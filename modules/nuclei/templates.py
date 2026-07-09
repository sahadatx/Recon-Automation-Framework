"""
Nuclei Template Manager

Manages built-in and custom
Nuclei template profiles.
"""

from pathlib import Path


# ==========================================================
# Built-in Profiles
# ==========================================================

DEFAULT = [

    "http/exposures",

]

FAST = [

    "http/exposures",

]

WEB = [

    "http/exposures",

    "http/default-logins",

]

DNS = [

    "dns",

]

SSL = [

    "ssl",

]

NETWORK = [

    "network",

]

HEADLESS = [

    "headless",

]

DAST = [

    "dast",

]

JAVASCRIPT = [

    "javascript",

]

FILE = [

    "file",

]

CLOUD = [

    "cloud",

]

CODE = [

    "code",

]

FULL = [

    ".",

]


# ==========================================================
# Available Profiles
# ==========================================================

AVAILABLE_PROFILES = {

    "default": DEFAULT,

    "fast": FAST,

    "web": WEB,

    "dns": DNS,

    "ssl": SSL,

    "network": NETWORK,

    "headless": HEADLESS,

    "dast": DAST,

    "javascript": JAVASCRIPT,

    "file": FILE,

    "cloud": CLOUD,

    "code": CODE,

    "full": FULL,

}


# ==========================================================
# Validation
# ==========================================================

def validate_directory(
    path: Path,
):
    """
    Validate directory.
    """

    return (

        path.exists()

        and

        path.is_dir()

    )


def validate_file(
    path: Path,
):
    """
    Validate file.
    """

    return (

        path.exists()

        and

        path.is_file()

    )


def validate_profile(
    profile: str,
):
    """
    Validate profile.
    """

    return (

        profile.lower()

        in

        AVAILABLE_PROFILES

    )


# ==========================================================
# Resolve Templates
# ==========================================================

def resolve_templates(
    templates: list[str],
):
    """
    Return template list.

    Nuclei resolves built-in
    template paths itself.
    """

    return list(
        templates
    )


# ==========================================================
# Get Templates
# ==========================================================

def get_templates(
    profile: str = "default",
    custom: str | None = None,
):
    """
    Return template list.

    Args:
        profile:
            Built-in profile.

        custom:
            Custom template file
            or directory.

    Returns:
        list[str | Path]
    """

    # ------------------------------------------------------
    # Custom Template
    # ------------------------------------------------------

    if custom:

        path = Path(
            custom
        )

        if validate_directory(
            path
        ):

            return [

                path,

            ]

        if validate_file(
            path
        ):

            return [

                path,

            ]

        raise FileNotFoundError(

            f"Template not found: {path}"

        )

    # ------------------------------------------------------
    # Built-in Profile
    # ------------------------------------------------------

    profile = profile.lower()

    if not validate_profile(
        profile
    ):

        raise ValueError(

            f"Unknown profile: {profile}"

        )

    return resolve_templates(

        AVAILABLE_PROFILES[
            profile
        ]

    )


# ==========================================================
# List Profiles
# ==========================================================

def list_profiles():
    """
    Return available profiles.
    """

    return sorted(

        AVAILABLE_PROFILES.keys()

    )


# ==========================================================
# List Templates
# ==========================================================

def list_templates(
    profile: str = "default",
):
    """
    Return templates for
    one profile.
    """

    if not validate_profile(
        profile
    ):

        return []

    return list(

        AVAILABLE_PROFILES[
            profile.lower()
        ]

    )


# ==========================================================
# List Categories
# ==========================================================

def list_categories():
    """
    Return all unique
    template categories.
    """

    categories = set()

    for templates in AVAILABLE_PROFILES.values():

        categories.update(
            templates
        )

    return sorted(
        categories
    )


# ==========================================================
# Template Exists
# ==========================================================

def template_exists(
    profile: str = "default",
):
    """
    Check profile exists.
    """

    return validate_profile(
        profile
    )


# ==========================================================
# Default Profile
# ==========================================================

def default_profile():
    """
    Return default profile.
    """

    return "default"


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    print()

    print(

        "=" * 60

    )

    print(

        "Nuclei Template Manager"

    )

    print(

        "=" * 60

    )

    print(

        "Profiles"

    )

    print(

        list_profiles()

    )

    print()

    print(

        "Categories"

    )

    print(

        list_categories()

    )

    print()

    print(

        "Default Profile :",

        default_profile(),

    )

    print()

    print(

        "Default Templates"

    )

    print(

        list_templates()

    )

    print()

    print(

        "Fast Templates"

    )

    print(

        list_templates(
            "fast"
        )

    )

    print()

    print(

        "Web Templates"

    )

    print(

        list_templates(
            "web"
        )

    )

    print()

    print(

        "=" * 60

    )
