"""
Report Statistics

Generate summary statistics for the final report.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Helpers
# ==========================================================

def _count(
    value: Any,
) -> int:
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

    modules = report.get(
        "modules",
        {},
    )

    passive = modules.get(
        "passive",
        {},
    )

    dns = modules.get(
        "dns",
        {},
    )

    http = modules.get(
        "http",
        {},
    )

    ports = modules.get(
        "ports",
        {},
    )

    technology = modules.get(
        "technology",
        {},
    )

    screenshots = modules.get(
        "screenshots",
        {},
    )

    urls = modules.get(
        "urls",
        {},
    )

    javascript = modules.get(
        "javascript",
        {},
    )

    directories = modules.get(
        "directories",
        {},
    )

    vhosts = modules.get(
        "vhosts",
        {},
    )

    tls = modules.get(
        "tls",
        {},
    )

    waf = modules.get(
        "waf",
        {},
    )

    cdn = modules.get(
        "cdn",
        {},
    )

    takeover = modules.get(
        "takeover",
        {},
    )

    email = modules.get(
        "email",
        {},
    )

    statistics = {

        "total_subdomains": passive.get(
            "statistics",
            {},
        ).get(
            "total_subdomains",
            _count(
                passive.get(
                    "results",
                    [],
                )
            ),
        ),

        "resolved_hosts": dns.get(
            "statistics",
            {},
        ).get(
            "resolved_hosts",
            0,
        ),

        "alive_hosts": http.get(
            "statistics",
            {},
        ).get(
            "alive_hosts",
            0,
        ),

        "open_ports": ports.get(
            "statistics",
            {},
        ).get(
            "total_open_ports",
            0,
        ),

        "technologies": technology.get(
            "statistics",
            {},
        ).get(
            "technology_count",
            0,
        ),

        "screenshots": screenshots.get(
            "statistics",
            {},
        ).get(
            "captured",
            0,
        ),

        "urls": urls.get(
            "statistics",
            {},
        ).get(
            "total_urls",
            0,
        ),

        "javascript_files": javascript.get(
            "statistics",
            {},
        ).get(
            "processed_files",
            0,
        ),

        "directories": directories.get(
            "statistics",
            {},
        ).get(
            "total_results",
            0,
        ),

        "virtual_hosts": vhosts.get(
            "statistics",
            {},
        ).get(
            "total_results",
            0,
        ),

        "tls_hosts": tls.get(
            "statistics",
            {},
        ).get(
            "targets",
            0,
        ),

        "waf_hosts": waf.get(
            "statistics",
            {},
        ).get(
            "detected",
            0,
        ),

        "cdn_hosts": cdn.get(
            "statistics",
            {},
        ).get(
            "detected",
            0,
        ),

        "takeover_candidates": takeover.get(
            "statistics",
            {},
        ).get(
            "vulnerable",
            0,
        ),

        "email_records": email.get(
            "statistics",
            {},
        ).get(
            "targets",
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

    lines.append(
        "=" * 80
    )

    return "\n".join(
        lines
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "generate_statistics",
    "generate_summary",
]