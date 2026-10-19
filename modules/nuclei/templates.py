from pathlib import Path


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


def validate_directory(
    path: Path,
):


    return path.exists() and path.is_dir()


def validate_file(
    path: Path,
):


    return path.exists() and path.is_file()


def validate_profile(
    profile: str,
):


    return profile.lower() in AVAILABLE_PROFILES


def resolve_templates(
    templates: list[str],
):


    return list(templates)


def get_templates(
    profile: str = "default",
    custom: str | None = None,
):


    if custom:

        path = Path(custom)

        if validate_directory(path):

            return [
                path,
            ]

        if validate_file(path):

            return [
                path,
            ]

        raise FileNotFoundError(f"Template not found: {path}")


    profile = profile.lower()

    if not validate_profile(profile):

        raise ValueError(f"Unknown profile: {profile}")

    return resolve_templates(AVAILABLE_PROFILES[profile])


def list_profiles():


    return sorted(AVAILABLE_PROFILES.keys())


def list_templates(
    profile: str = "default",
):


    if not validate_profile(profile):

        return []

    return list(AVAILABLE_PROFILES[profile.lower()])


def list_categories():


    categories = set()

    for templates in AVAILABLE_PROFILES.values():

        categories.update(templates)

    return sorted(categories)


def template_exists(
    profile: str = "default",
):


    return validate_profile(profile)


def default_profile():


    return "default"


if __name__ == "__main__":

    print()

    print("=" * 60)

    print("Nuclei Template Manager")

    print("=" * 60)

    print("Profiles")

    print(list_profiles())

    print()

    print("Categories")

    print(list_categories())

    print()

    print(
        "Default Profile :",
        default_profile(),
    )

    print()

    print("Default Templates")

    print(list_templates())

    print()

    print("Fast Templates")

    print(list_templates("fast"))

    print()

    print("Web Templates")

    print(list_templates("web"))

    print()

    print("=" * 60)
