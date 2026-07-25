#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

from __future__ import annotations

import argparse
from typing import Any, Callable

from core.analysis import (
    empty_analysis,
    empty_list_analysis,
)

from core.banner import show_banner

from core.logger import (
    info,
    warning,
)

# ==========================================================
# Passive Enumeration
# ==========================================================

from modules.passive.manager import (
    run as run_passive,
)

# ==========================================================
# DNS Resolution
# ==========================================================

from modules.dns.manager import (
    run as run_dns,
)

# ==========================================================
# HTTP Probe
# ==========================================================

from modules.http.manager import (
    run as run_http,
)

# ==========================================================
# Port Scanner
# ==========================================================

from modules.ports.manager import (
    run as run_ports,
)

# ==========================================================
# Technology Detection
# ==========================================================

from modules.tech.manager import (
    run as run_technology,
)

# ==========================================================
# URL Discovery
# ==========================================================

from modules.crawler.manager import (
    run as run_crawler,
)

# ==========================================================
# JavaScript Analysis
# ==========================================================

from modules.javascript.manager import (
    run as run_javascript,
)

# ==========================================================
# Directory Fuzzing
# ==========================================================

from modules.fuzzing.manager import (
    run_fuzzing,
)

from modules.fuzzing.exporter import (
    export_all as export_fuzzing_results,
)

# ==========================================================
# Screenshot Capture
# ==========================================================

from modules.screenshots.manager import (
    execute as run_screenshot,
)

# ==========================================================
# Virtual Host Discovery
# ==========================================================

from modules.vhost.manager import (
    run_vhosts,
)

# ==========================================================
# Nuclei Scanner
# ==========================================================

from modules.nuclei.manager import (
    run_nuclei,
)

from modules.nuclei.exporter import (
    export_all as export_nuclei_results,
)

# ==========================================================
# WAF Detection
# ==========================================================

from modules.waf.manager import (
    run_waf_detection,
)

# ==========================================================
# TLS Analysis
# ==========================================================

from modules.tls.manager import (
    run_tls_analysis,
)

# ==========================================================
# CDN Detection
# ==========================================================

from modules.cdn.manager import (
    run_cdn_detection,
)

# ==========================================================
# Subdomain Takeover Detection
# ==========================================================

from modules.takeover.manager import (
    run_takeover_detection,
)

from modules.takeover.exporter import (
    export_all as export_takeover_results,
)

# ==========================================================
# Email Security
# ==========================================================

from modules.email.manager import (
    run_email_security,
)

# ==========================================================
# Report Generator
# ==========================================================

from modules.report.manager import (
    execute as run_report,
)

# ==========================================================
# Dashboard
# ==========================================================

from modules.dashboard.manager import (
    run_dashboard,
)

# ==========================================================
# Helpers
# ==========================================================


def run_module(
    module_name: str,
    runner: Callable[..., dict[str, Any]],
    *args: Any,
    empty_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Execute a module safely.

    Args:
        module_name:
            Friendly module name.

        runner:
            Module entry function.

        *args:
            Arguments passed to the module.

        empty_result:
            Optional fallback result.

    Returns:
        Analysis dictionary.
    """

    try:
        return runner(*args)

    except Exception as error:

        warning(
            f"{module_name} failed: {error}"
        )

        if empty_result is None:
            return empty_analysis()

        return empty_result


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

    passive_analysis = run_passive(
        args.domain,
    )

    unique_subdomains = passive_analysis[
         "results"
    ]

    # ------------------------------------------------------
    # DNS Resolution
    # ------------------------------------------------------

    dns_analysis = run_dns(
        unique_subdomains,
    )

    dns_results = dns_analysis[
        "results"
    ]

    # ------------------------------------------------------
    # HTTP Probe
    # ------------------------------------------------------

    http_hosts = list(
        dns_results.keys()
    )

    http_analysis = run_http(
        http_hosts,
    )

    http_results = http_analysis[
        "results"
    ]


    # ------------------------------------------------------
    # Live HTTP URLs
    # ------------------------------------------------------

    live_urls = sorted(
        {
            result["url"]
            for result in http_results.values()
            if result.get("url")
        }
    )

    info(
        f"Live HTTP Targets: {len(live_urls)}"
    )

    # ------------------------------------------------------
    # Port Scanner
    # ------------------------------------------------------

    port_hosts = list(
        http_results.keys()
    )

    port_analysis = run_ports(
        port_hosts,
    )

    port_results = port_analysis[
        "results"
    ]

    # ------------------------------------------------------
    # Technology Detection
    # ------------------------------------------------------

    technology_analysis = run_technology(
        http_results,
    )

    technology_results = technology_analysis[
        "results"
    ]

    # ------------------------------------------------------
    # URL Discovery
    # ------------------------------------------------------

    info(
        f"Crawl Targets: {len(live_urls)}"
    )

    if live_urls:

        crawl_analysis = run_module(
            "URL Discovery",
            run_crawler,
            live_urls,
        )

    else:

        info(
            "No crawl targets discovered."
        )

        crawl_analysis = empty_analysis()

    # ------------------------------------------------------
    # JavaScript Analysis
    # ------------------------------------------------------

    javascript_urls = sorted(
        {
            script
            for host in crawl_analysis.get(
                "results",
                {},
            ).values()
            for page in host.get(
                "pages",
                {},
            ).values()
            for script in page.get(
                "parsed",
                {},
            ).get(
                "javascript",
                [],
            )
        }
    )

    info(
        f"JavaScript Targets: {len(javascript_urls)}"
    )

    if javascript_urls:

        javascript_analysis = run_module(
            "JavaScript Analysis",
            run_javascript,
            javascript_urls,
        )

    else:

        info(
            "No JavaScript files discovered."
        )

        javascript_analysis = empty_analysis()


    # ------------------------------------------------------
    # Directory Fuzzing
    # ------------------------------------------------------

    info(
        f"Directory Fuzzing Targets: {len(live_urls)}"
    )

    if live_urls:

        directory_analysis = run_module(
            "Directory Fuzzing",
            run_fuzzing,
            live_urls,
        )

        export_fuzzing_results(
            directory_analysis,
        )

    else:

        info(
            "No fuzzing targets discovered."
        )

        directory_analysis = empty_analysis()

    # ------------------------------------------------------
    # Screenshot Capture
    # ------------------------------------------------------

    if live_urls:

        screenshot_analysis = run_module(
            "Screenshot Capture",
            run_screenshot,
            http_results,
            empty_result=empty_list_analysis(),
        )

    else:

        info(
            "No alive hosts for screenshots."
        )

        screenshot_analysis = empty_list_analysis()

    # ------------------------------------------------------
    # Virtual Host Discovery
    # ------------------------------------------------------

    info(
        f"Virtual Host Targets: {len(live_urls)}"
    )

    if live_urls:

        vhost_analysis = run_module(
            "Virtual Host Discovery",
            run_vhosts,
            live_urls,
        )

    else:

        info(
            "No targets for Virtual Host Discovery."
        )

        vhost_analysis = empty_analysis()

    # ------------------------------------------------------
    # Nuclei Scan
    # ------------------------------------------------------

    info(
        f"Nuclei Targets: {len(live_urls)}"
    )

    if live_urls:

        nuclei_analysis = run_module(
            "Nuclei Scanner",
            run_nuclei,
            live_urls,
        )

        export_nuclei_results(
            nuclei_analysis,
        )

    else:

        info(
            "No targets for Nuclei scan."
        )

        nuclei_analysis = empty_analysis()

    # ------------------------------------------------------
    # WAF Detection
    # ------------------------------------------------------

    info(
        f"WAF Targets: {len(live_urls)}"
    )

    if live_urls:

        waf_analysis = run_module(
            "WAF Detection",
            run_waf_detection,
            live_urls,
        )

    else:

        info(
            "No targets for WAF Detection."
        )

        waf_analysis = empty_analysis()

    # ------------------------------------------------------
    # TLS Analysis
    # ------------------------------------------------------

    info(
        f"TLS Targets: {len(live_urls)}"
    )

    if live_urls:

        tls_analysis = run_module(
            "TLS Analysis",
            run_tls_analysis,
            live_urls,
        )

    else:

        info(
            "No targets for TLS Analysis."
        )

        tls_analysis = empty_analysis()

    # ------------------------------------------------------
    # CDN Detection
    # ------------------------------------------------------

    info(
        f"CDN Targets: {len(live_urls)}"
    )

    if live_urls:

        cdn_analysis = run_module(
            "CDN Detection",
            run_cdn_detection,
            live_urls,
        )

    else:

        info(
            "No targets for CDN Detection."
        )

        cdn_analysis = empty_analysis()

    # ------------------------------------------------------
    # Subdomain Takeover Detection
    # ------------------------------------------------------

    info(
        f"Takeover Targets: {len(live_urls)}"
    )

    if live_urls:

        takeover_analysis = run_module(
            "Subdomain Takeover Detection",
            run_takeover_detection,
            live_urls,
        )

        export_takeover_results(
            takeover_analysis,
        )


    else:

        info(
            "No targets for Takeover Detection."
        )

        takeover_analysis = empty_analysis()

    # ------------------------------------------------------
    # Email Security
    # ------------------------------------------------------

    info(
        f"Email Targets: {len(live_urls)}"
    )

    if live_urls:

        email_analysis = run_module(
            "Email Security",
            run_email_security,
            live_urls,
        )

    else:

        info(
            "No targets for Email Security."
        )

        email_analysis = empty_analysis()


    # ==========================================================
    # Report Generator
    # ==========================================================

    analysis = {

        "passive": passive_analysis,

        "dns": dns_analysis,

        "http": http_analysis,

        "ports": port_analysis,

        "technology": technology_analysis,

        "urls": crawl_analysis,

        "javascript": javascript_analysis,

        "directories": directory_analysis,

        "screenshots": screenshot_analysis,

        "vhosts": vhost_analysis,

        "nuclei": nuclei_analysis,

        "tls": tls_analysis,

        "waf": waf_analysis,

        "cdn": cdn_analysis,

        "takeover": takeover_analysis,

        "email": email_analysis,

    }

    report_analysis = run_report(
        analysis,
    )

    dashboard_analysis = run_dashboard()


# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":

    main()

