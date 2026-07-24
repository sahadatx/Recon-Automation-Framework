#!/usr/bin/env python3

"""
Recon Automation Framework

Main Entry Point
"""

import argparse

import asyncio

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
    show_summary as show_fuzzing_summary,
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

    run_and_export,

    print_summary,

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

# ==========================================================
# Email Security
# ==========================================================

from modules.email.manager import (

    run_email_security,

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

    passive_analysis = run_passive(
        args.domain,
    )

    unique_subdomains = passive_analysis[
        "subdomains"
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

    live_urls = sorted({

        result["url"]

        for result in http_results.values()

        if result.get(
            "url"
        )

    })

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

    technology_results = (
        technology_analysis[
            "results"
        ]
    )


    # ------------------------------------------------------
    # URL Discovery
    # ------------------------------------------------------

    info(
        f"Crawl Targets: {len(live_urls)}"
    )

    if live_urls:

        crawl_analysis = run_crawler(
            live_urls,
        )

    else:

        info(
            "No crawl targets discovered."
        )

        crawl_analysis = {
            "results": {},
            "statistics": {},
        }


    # ------------------------------------------------------
    # JavaScript Analysis
    # ------------------------------------------------------

    javascript_urls = sorted({

        script

        for host in crawl_analysis.get(
            "results", {}
        ).values()

        for page in host.get(
            "pages", {}
        ).values()

        for script in page.get(
            "parsed", {}
        ).get(
            "javascript", []
        )

    })

    if javascript_urls:

        javascript_analysis = run_javascript(
            javascript_urls
        )

    else:

        info(
            "No JavaScript files discovered."
        )

    # ------------------------------------------------------
    # Directory Fuzzing
    # ------------------------------------------------------

    if live_urls:

        try:

            (

                fuzz_results,

                fuzz_statistics,

                fuzz_failed,

                fuzz_time,

            ) = run_fuzzing(

                live_urls

            )

            export_fuzzing_results(

                fuzz_results

            )

            show_fuzzing_summary(

                fuzz_results,

                fuzz_statistics,

                fuzz_failed,

                fuzz_time,

            )

        except Exception as error:

            warning(

                f"Directory Fuzzing failed: {error}"

            )

    else:

        info(

            "No fuzzing targets discovered."

        )

    # ------------------------------------------------------
    # Screenshot Capture
    # ------------------------------------------------------

    if live_urls:

        screenshot_analysis = run_screenshot(

            http_results

        )


    else:

        info(

            "No alive hosts for screenshots."

        )

        screenshot_analysis = {

            "total_targets": 0,

            "captured": 0,

            "failed": 0,

            "results": {},

        }
    


    # ------------------------------------------------------
    # Virtual Host Discovery
    # ------------------------------------------------------

    info(

        f"Virtual Host Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_vhosts(

                live_urls

            )

        except Exception as error:

            warning(

                f"Virtual Host Discovery failed: {error}"

            )

    else:

        info(

            "No targets for Virtual Host Discovery."

        )



    # ------------------------------------------------------
    # Nuclei Scan
    # ------------------------------------------------------

    info(

        f"Nuclei Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            (

                _,

                nuclei_overall,

                _,

                _,

                _,

            ) = run_and_export(

                live_urls

            )

            print_summary(

                nuclei_overall

            )

        except Exception as error:

            warning(

                f"Nuclei scan failed: {error}"

            )

    else:

        info(

            "No targets for Nuclei scan."

        )



    # ------------------------------------------------------
    # WAF Detection
    # ------------------------------------------------------

    info(

        f"WAF Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_waf_detection(

                live_urls

            )

        except Exception as error:

            warning(

                f"WAF Detection failed: {error}"

            )

    else:

        info(

            "No targets for WAF Detection."

        )


    # ==========================================================
    # TLS Analysis
    # ==========================================================

    info(

        f"TLS Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_tls_analysis(

                live_urls

            )

        except Exception as error:

            warning(

                f"TLS Analysis failed: {error}"

            )

    else:

        info(

            "No targets for TLS Analysis."

        )



    # ==========================================================
    # CDN Detection
    # ==========================================================

    info(

        f"CDN Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_cdn_detection(

                live_urls,

            )

        except Exception as error:

            warning(

                f"CDN Detection failed: {error}"

            )

    else:

        info(

            "No targets for CDN Detection."

        )



    # ==========================================================
    # Subdomain Takeover Detection
    # ==========================================================

    info(

        f"Takeover Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_takeover_detection(

                live_urls,

            )

        except Exception as error:

            warning(

                f"Takeover Detection failed: {error}"

            )

    else:

        info(

            "No targets for Takeover Detection."

        )


    # ==========================================================
    # Email Security
    # ==========================================================

    info(

        f"Email Targets: {len(live_urls)}"

    )

    if live_urls:

        try:

            run_email_security(

                live_urls,

            )

        except Exception as error:

            warning(

                f"Email Security failed: {error}"

            )

    else:

        info(

            "No targets for Email Security."

        )

# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()


