"""
Report Statistics

Generate summary statistics for the final report.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Helpers
# ==========================================================


def _count(value: Any) -> int:
    """
    Return the number of items in a collection.
    """

    if value is None:
        return 0

    if isinstance(
        value,
        (list, tuple, set, dict),
    ):
        return len(value)

    return 1


# ==========================================================
# Statistics
# ==========================================================


def generate_statistics(
    report: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate report statistics.
    """

    passive = report.get("passive", {})
    dns = report.get("dns", {})
    http = report.get("http", {})
    ports = report.get("ports", {})
    technology = report.get("technology", {})
    screenshots = report.get("screenshots", {})
    urls = report.get("urls", {})
    javascript = report.get("javascript", {})
    directories = report.get("directories", {})
    vhosts = report.get("vhosts", {})
    tls = report.get("tls", {})
    waf = report.get("waf", {})
    cdn = report.get("cdn", {})
    takeover = report.get("takeover", {})
    email = report.get("email", {})

    statistics = {

        "total_subdomains": passive.get(
            "total_subdomains",
            _count(
                passive.get(
                    "results",
                    {},
                )
            ),
        ),

        "resolved_hosts": dns.get(
            "resolved",
            0,
        ),

        "alive_hosts": http.get(
            "alive",
            0,
        ),

        "open_ports": ports.get(
            "open_ports",
            0,
        ),

        "technologies": technology.get(
            "total_technologies",
            0,
        ),

        "screenshots": screenshots.get(
            "captured",
            0,
        ),

        "urls": urls.get(
            "total_urls",
            0,
        ),

        "javascript_files": javascript.get(
            "processed_files",
            0,
        ),

        "directories": directories.get(
            "found_directories",
            0,
        ),

        "virtual_hosts": vhosts.get(
            "total_vhosts",
            0,
        ),

        "tls_hosts": tls.get(
            "analyzed_hosts",
            0,
        ),

        "waf_hosts": waf.get(
            "detected_hosts",
            0,
        ),

        "cdn_hosts": cdn.get(
            "detected_hosts",
            0,
        ),

        "takeover_candidates": takeover.get(
            "possible_takeovers",
            0,
        ),

        "email_records": email.get(
            "total_records",
            0,
        ),

    }

    return statistics


# ==========================================================
# Summary
# ==========================================================


def generate_summary(
    statistics: dict[str, Any],
) -> str:
    """
    Generate a printable summary.
    """

    lines = [

        "=" * 80,
        "Recon Automation Framework Report Summary",
        "=" * 80,

    ]

    for key, value in statistics.items():

        name = key.replace(
            "_",
            " ",
        ).title()

        lines.append(
            f"{name:<30} {value}"
        )

    lines.append("=" * 80)

    return "\n".join(lines)


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "generate_statistics",
    "generate_summary",
]