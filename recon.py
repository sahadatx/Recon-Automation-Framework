from core.banner import show_banner
from core.logger import info
from core.utils import (
    create_directory,
    read_file,
    write_file,
    validate_domain,
)


def main():

    show_banner()

    create_directory("output")

    domains = [
        "example.com",
        "google.com",
    ]

    write_file(
        "output/domains.txt",
        domains
    )

    data = read_file(
        "output/domains.txt"
    )

    info(f"Domains: {data}")

    info(
        f"example.com valid: "
        f"{validate_domain('example.com')}"
    )


if __name__ == "__main__":
    main()