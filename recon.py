#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

import argparse

from core.banner import show_banner

# ==========================================================
# Passive Enumeration
# ==========================================================

from modules.passive.manager import (
    collect_subdomains,
    merge_results,
    save_results,
    export_results,
    show_summary as show_passive_summary,
)

# ==========================================================
# DNS Resolution
# ==========================================================

from modules.dns.manager import (
    resolve_subdomains,
    save_dns_results,
    export_dns_json,
    show_summary as show_dns_summary,
)


# ==========================================================
# Main
# ==========================================================

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

    # ------------------------------------------------------
    # Banner
    # ------------------------------------------------------

    show_banner()

    # ------------------------------------------------------
    # Passive Enumeration
    # ------------------------------------------------------

    results, timings, failed, total_time = collect_subdomains(
        args.domain
    )

    unique = merge_results(results)

    save_results(unique)

    export_results(results)

    show_passive_summary(
        results,
        timings,
        failed,
        unique,
        total_time,
    )

    # ------------------------------------------------------
    # DNS Resolution
    # ------------------------------------------------------

    dns_results, dns_failed, dns_time = resolve_subdomains(
        unique
    )

    save_dns_results(
        dns_results
    )

    export_dns_json(
        dns_results
    )

    show_dns_summary(
        dns_results,
        dns_failed,
        dns_time,
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()