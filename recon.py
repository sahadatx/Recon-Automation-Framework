#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

import argparse

from core.banner import show_banner

from modules.passive.manager import (
    collect_subdomains,
    merge_results,
    save_results,
    export_results,
    show_summary,
)


def main() -> None:
    """
    Main function.
    """

    parser = argparse.ArgumentParser(
        prog="recon",
        description="Recon Automation Framework",
    )

    parser.add_argument(
        "-d",
        "--domain",
        required=True,
        metavar="DOMAIN",
        help="Target domain (e.g. example.com)",
    )

    args = parser.parse_args()

    show_banner()

    results, timings, failed, total_time = collect_subdomains(
        args.domain
    )

    unique = merge_results(results)

    save_results(unique)

    export_results(results)

    show_summary(
        results,
        timings,
        failed,
        unique,
        total_time,
    )


if __name__ == "__main__":
    main()