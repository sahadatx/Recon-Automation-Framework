"""
Nuclei Updater

Handles template installation,
updates and version checking.
"""

import subprocess

from pathlib import Path

from modules.nuclei.helpers import (
    ensure_directory,
)


# ==========================================================
# Default Template Directory
# ==========================================================

DEFAULT_TEMPLATE_DIRECTORY = (

    Path.home()

    / "nuclei-templates"

)


# ==========================================================
# Get Template Directory
# ==========================================================

def get_templates_directory():
    """
    Return template directory.

    Returns:
        Path
    """

    ensure_directory(

        DEFAULT_TEMPLATE_DIRECTORY

    )

    return DEFAULT_TEMPLATE_DIRECTORY


# ==========================================================
# Check Templates
# ==========================================================

def is_templates_installed():
    """
    Check whether templates
    exist.

    Returns:
        bool
    """

    directory = (

        get_templates_directory()

    )

    return any(

        directory.iterdir()

    )


# ==========================================================
# Get Template Version
# ==========================================================

def get_templates_version():
    """
    Return installed template
    version.

    Returns:
        str | None
    """

    version_file = (

        get_templates_directory()

        / ".version"

    )

    if not version_file.exists():

        return None

    try:

        return (

            version_file

            .read_text(

                encoding="utf-8",

            )

            .strip()

        )

    except Exception:

        return None


# ==========================================================
# Install Templates
# ==========================================================

def install_templates():
    """
    Install templates.

    Returns:
        bool
    """

    try:

        result = subprocess.run(

            [

                "nuclei",

                "-update-templates",

            ],

            capture_output=True,

            text=True,

            timeout=600,

        )

        return (

            result.returncode == 0

        )

    except Exception:

        return False


# ==========================================================
# Update Templates
# ==========================================================

def update_templates():
    """
    Update installed
    templates.

    Returns:
        bool
    """

    return install_templates()


# ==========================================================
# Check For Updates
# ==========================================================

def check_for_updates():
    """
    Check whether template
    updates are available.

    Returns:
        bool | None

        True:
            Update available.

        False:
            Already up-to-date.

        None:
            Check failed.
    """

    try:

        result = subprocess.run(

            [

                "nuclei",

                "-update-templates",

            ],

            capture_output=True,

            text=True,

            timeout=600,

        )

        output = (

            result.stdout

            + result.stderr

        ).lower()

        if result.returncode != 0:

            return None

        if (

            "already"

            in output

            or

            "up-to-date"

            in output

        ):

            return False

        return True

    except Exception:

        return None


# ==========================================================
# Auto Update
# ==========================================================

def auto_update():
    """
    Install templates if
    missing, otherwise update.

    Returns:
        bool
    """

    if not is_templates_installed():

        return install_templates()

    return update_templates()


# ==========================================================
# Show Status
# ==========================================================

def show_status():
    """
    Display template status.

    Returns:
        dict
    """

    status = {

        "installed":

            is_templates_installed(),

        "directory":

            str(

                get_templates_directory()

            ),

        "version":

            get_templates_version(),

    }

    print()

    print("=" * 60)

    print(
        "Nuclei Templates"
    )

    print("=" * 60)

    print(

        f"{'Installed':<20}"

        f"{status['installed']}"

    )

    print(

        f"{'Directory':<20}"

        f"{status['directory']}"

    )

    print(

        f"{'Version':<20}"

        f"{status['version']}"

    )

    print("=" * 60)

    return status


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    show_status()

    print()

    print(

        "Checking for updates..."

    )

    update = check_for_updates()

    if update is True:

        print(

            "Updates available."

        )

    elif update is False:

        print(

            "Templates are already up-to-date."

        )

    else:

        print(

            "Unable to check for updates."

        )