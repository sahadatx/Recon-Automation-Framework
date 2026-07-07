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
# Port Scanner
# ==========================================================

from modules.ports.manager import (
    scan_hosts,
)

from modules.ports.exporter import (
    save_open_ports,
    save_port_results,
    export_port_json,
    export_open_ports_csv,
    show_summary as show_port_summary,
)


# ==========================================================
# Technology Detection
# ==========================================================

from modules.tech.manager import (
    detect_hosts,
)

from modules.tech.exporter import (
    save_technologies,
    save_technology_results,
    export_technology_json,
    export_technology_csv,
    show_summary as show_technology_summary,
)


# ==========================================================
# Screenshot Capture
# ==========================================================

from modules.screenshot.manager import (
    capture_hosts,
)

from modules.screenshot.exporter import (
    save_screenshot_results,
    export_screenshot_json,
    show_summary as show_screenshot_summary,
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

    http_hosts = list(
        dns_results.keys()
    )

    http_results, http_failed, http_time = (
        probe_hosts(
            http_hosts
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

    # ------------------------------------------------------
    # Port Scanner
    # ------------------------------------------------------

    port_hosts = list(
        http_results.keys()
    )

    port_results, port_failed, port_time = (
        scan_hosts(
            port_hosts
        )
    )

    save_open_ports(
        port_results
    )

    save_port_results(
        port_results
    )

    export_port_json(
        port_results
    )

    export_open_ports_csv(
        port_results
    )

    show_port_summary(
        port_results,
        port_failed,
        port_time,
    )

    # ------------------------------------------------------
    # Technology Detection
    # ------------------------------------------------------

    technology_results, technology_failed, technology_time = (
        detect_hosts(
            http_results
        )
    )

    save_technologies(
        technology_results
    )

    save_technology_results(
        technology_results
    )

    export_technology_json(
        technology_results
    )

    export_technology_csv(
        technology_results
    )

    show_technology_summary(
        technology_results,
        technology_failed,
        technology_time,
    )

    # ------------------------------------------------------
    # Screenshot Capture
    # ------------------------------------------------------

    screenshot_results, screenshot_failed, screenshot_time = (
        capture_hosts(
            http_results
        )
    )

    save_screenshot_results(
        screenshot_results
    )

    export_screenshot_json(
        screenshot_results
    )

    show_screenshot_summary(
        screenshot_results,
        screenshot_failed,
        screenshot_time,
    )


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()