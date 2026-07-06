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
# HTTP Probe
# ==========================================================

from modules.http.manager import (
    probe_hosts,
)

from modules.http.exporter import (
    save_alive_hosts,
    save_http_results,
    export_http_json,
    show_summary as show_http_summary,
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

    passive_results, timings, passive_failed, passive_time = (
        collect_subdomains(
            args.domain
        )
    )

    unique_subdomains = merge_results(
        passive_results
    )

    save_results(
        unique_subdomains
    )

    export_results(
        passive_results
    )

    show_passive_summary(
        passive_results,
        timings,
        passive_failed,
        unique_subdomains,
        passive_time,
    )

    # ------------------------------------------------------
    # DNS Resolution
    # ------------------------------------------------------

    dns_results, dns_failed, dns_time = (
        resolve_subdomains(
            unique_subdomains
        )
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

    # ------------------------------------------------------
    # HTTP Probe
    # ------------------------------------------------------

    # Probe only DNS-resolved hosts

    hosts = list(
        dns_results.keys()
    )

    http_results, http_failed, http_time = (
        probe_hosts(
            hosts
        )
    )

    save_alive_hosts(
        http_results
    )

    save_http_results(
        http_results
    )

    export_http_json(
        http_results
    )

    show_http_summary(
        http_results,
        http_failed,
        http_time,
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()