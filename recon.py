from core.banner import show_banner
from core.logger import (
    info,
    success,
    warning,
    error,
    debug,
)


def main():

    show_banner()

    info("Initializing framework...")

    success("Logger loaded successfully.")

    warning("This is a sample warning.")

    error("This is a sample error.")

    debug("Debug mode enabled.")


if __name__ == "__main__":
    main()