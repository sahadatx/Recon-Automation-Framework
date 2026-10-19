import subprocess
from pathlib import Path

from modules.nuclei.helpers import ensure_directory


DEFAULT_TEMPLATE_DIRECTORY = Path.home() / "nuclei-templates"


def get_templates_directory():


    ensure_directory(DEFAULT_TEMPLATE_DIRECTORY)

    return DEFAULT_TEMPLATE_DIRECTORY


def is_templates_installed():


    directory = get_templates_directory()

    return any(directory.iterdir())


def get_templates_version():


    version_file = get_templates_directory() / ".version"

    if not version_file.exists():

        return None

    try:

        return version_file.read_text(
            encoding="utf-8",
        ).strip()

    except Exception:

        return None


def install_templates():


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

        return result.returncode == 0

    except Exception:

        return False


def update_templates():


    return install_templates()


def check_for_updates():


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

        output = (result.stdout + result.stderr).lower()

        if result.returncode != 0:

            return None

        if "already" in output or "up-to-date" in output:

            return False

        return True

    except Exception:

        return None


def auto_update():


    if not is_templates_installed():

        return install_templates()

    return update_templates()


def show_status():


    status = {
        "installed": is_templates_installed(),
        "directory": str(get_templates_directory()),
        "version": get_templates_version(),
    }

    print()

    print("=" * 60)

    print("Nuclei Templates")

    print("=" * 60)

    print(f"{'Installed':<20}" f"{status['installed']}")

    print(f"{'Directory':<20}" f"{status['directory']}")

    print(f"{'Version':<20}" f"{status['version']}")

    print("=" * 60)

    return status


if __name__ == "__main__":

    show_status()

    print()

    print("Checking for updates...")

    update = check_for_updates()

    if update is True:

        print("Updates available.")

    elif update is False:

        print("Templates are already up-to-date.")

    else:

        print("Unable to check for updates.")
