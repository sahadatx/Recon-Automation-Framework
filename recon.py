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
# URL Discovery
# ==========================================================

from modules.crawler.manager import (
    crawl_hosts,
)

from modules.crawler.exporter import (
    export_all as export_crawler_results,
)


# ==========================================================
# JavaScript Analysis
# ==========================================================

from modules.javascript.manager import (
    download_javascript,
)

from modules.javascript.exporter import (
    export_all as export_javascript_results,
    show_summary as show_javascript_summary,
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

from modules.screenshot.manager import (
    capture_hosts,
)

from modules.screenshot.exporter import (
    save_screenshot_results,
    export_screenshot_json,
    show_summary as show_screenshot_summary,
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
        passive_results,
        args.domain,
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
    # URL Discovery
    # ------------------------------------------------------

    info(

        f"Crawl Targets: {len(live_urls)}"

    )

    if live_urls:

        crawl_results = crawl_hosts(

            live_urls

        )

    else:

        info(

            "No crawl targets discovered."

        )

        crawl_results = {

            "results": {}

        }

    export_crawler_results(

        crawl_results

    )



    # ------------------------------------------------------
    # JavaScript Analysis
    # ------------------------------------------------------

    javascript_urls = sorted({

        script

        for host in crawl_results.get(

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

    })

    if javascript_urls:

        javascript_results, javascript_failed, javascript_time = (

            download_javascript(

                javascript_urls

            )

        )

        export_javascript_results(

            javascript_results

        )

        show_javascript_summary(

            javascript_results,

            javascript_failed,

            javascript_time,

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

        screenshot_results, screenshot_failed, screenshot_time = (

            asyncio.run(

                capture_hosts(

                    http_results

                )

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

    else:

        info(

            "No alive hosts for screenshots."

        )
    


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
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()


