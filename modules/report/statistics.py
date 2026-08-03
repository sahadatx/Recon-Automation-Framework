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


def _module(
    modules: dict[str, Any],
    name: str,
) -> dict[str, Any]:
    """
    Safely return a module analysis.
    """

    module = modules.get(
        name,
        {},
    )

    if isinstance(
        module,
        dict,
    ):

        return module

    return {}


def _stat(
    module: dict[str, Any],
    key: str,
    default: int = 0,
) -> int:
    """
    Return one statistic from a module.
    """

    return module.get(
        "statistics",
        {},
    ).get(
        key,
        default,
    )


# ==========================================================
# Statistics
# ==========================================================


def generate_statistics(
    report: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate summary statistics from
    all module analyses.
    """

    analyses = report.get(
        "modules",
        {},
    ).get(
        "analysis",
        {},
    )

    passive = _module(
        analyses,
        "passive",
    )

    dns = _module(
        analyses,
        "dns",
    )

    http = _module(
        analyses,
        "http",
    )

    ports = _module(
        analyses,
        "ports",
    )

    tech = _module(
        analyses,
        "tech",
    )

    crawler = _module(
        analyses,
        "crawler",
    )

    javascript = _module(
        analyses,
        "javascript",
    )

    fuzzing = _module(
        analyses,
        "fuzzing",
    )

    vhost = _module(
        analyses,
        "vhost",
    )

    screenshots = _module(
        analyses,
        "screenshots",
    )

    tls = _module(
        analyses,
        "tls",
    )

    waf = _module(
        analyses,
        "waf",
    )

    cdn = _module(
        analyses,
        "cdn",
    )

    takeover = _module(
        analyses,
        "takeover",
    )

    email = _module(
        analyses,
        "email",
    )

    statistics = {
        # --------------------------------------------------
        # Enumeration
        # --------------------------------------------------
        "total_subdomains": _stat(
            passive,
            "total_subdomains",
            _count(
                passive.get(
                    "results",
                    [],
                )
            ),
        ),
        "resolved_hosts": _stat(
            dns,
            "resolved_hosts",
        ),
        "alive_hosts": _stat(
            http,
            "alive_hosts",
        ),
        "open_ports": _stat(
            ports,
            "total_open_ports",
        ),
        # --------------------------------------------------
        # Discovery
        # --------------------------------------------------
        "technologies": _stat(
            tech,
            "technology_count",
        ),
        "urls": _stat(
            crawler,
            "total_urls",
        ),
        "javascript_files": _stat(
            javascript,
            "processed_files",
        ),
        "directories": _stat(
            fuzzing,
            "total_results",
        ),
        "virtual_hosts": _stat(
            vhost,
            "total_results",
        ),
        "screenshots": _stat(
            screenshots,
            "captured",
        ),
        # --------------------------------------------------
        # Security
        # --------------------------------------------------
        "tls_hosts": _stat(
            tls,
            "targets",
        ),
        "waf_hosts": _stat(
            waf,
            "detected",
        ),
        "cdn_hosts": _stat(
            cdn,
            "detected",
        ),
        "takeover_candidates": _stat(
            takeover,
            "vulnerable",
        ),
        "email_records": _stat(
            email,
            "targets",
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
    Generate a printable statistics summary.
    """

    lines = [
        "=" * 80,
        "Recon Automation Framework Report Summary",
        "=" * 80,
    ]

    labels = {
        "total_subdomains": "Total Subdomains",
        "resolved_hosts": "Resolved Hosts",
        "alive_hosts": "Alive Hosts",
        "open_ports": "Open Ports",
        "technologies": "Technologies",
        "screenshots": "Screenshots",
        "urls": "URLs",
        "javascript_files": "JavaScript Files",
        "directories": "Directories",
        "virtual_hosts": "Virtual Hosts",
        "tls_hosts": "TLS Hosts",
        "waf_hosts": "WAF Hosts",
        "cdn_hosts": "CDN Hosts",
        "takeover_candidates": "Takeover Candidates",
        "email_records": "Email Records",
    }

    for key, label in labels.items():

        lines.append(f"{label:<30} " f"{statistics.get(key, 0)}")

    lines.append("=" * 80)

    return "\n".join(
        lines,
    )


# ==========================================================
# Public API
# ==========================================================

__all__ = [
    "generate_statistics",
    "generate_summary",
]
