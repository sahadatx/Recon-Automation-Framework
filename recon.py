#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

import argparse
import sys
import time

from core.banner import show_banner
from core.logger import (
    info,
    success,
    error,
)
from core.utils import validate_domain


def parse_arguments():
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        prog="recon.py",
        description="Professional Recon Automation Framework"
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        help="Target domain"
    )

    return parser.parse_args()


def main():
    """
    Main workflow.
    """

    start_time = time.time()

    # Display Banner
    show_banner()

    # Parse CLI
    args = parse_arguments()

    domain = args.domain.strip().lower()

    # Validate Domain
    if not validate_domain(domain):
        error(f"Invalid domain: {domain}")
        sys.exit(1)

    # Display Target
    info(f"Target Domain : {domain}")

    # Placeholder
    info("Framework initialized successfully.")
    info("Passive Enumeration module will be added in Lesson 2.")

    elapsed = round(time.time() - start_time, 2)

    success(f"Finished in {elapsed} seconds.")


if __name__ == "__main__":
    main()