"""
Nuclei Statistics

Generates statistics from
Nuclei findings.
"""

from __future__ import annotations

from collections import Counter

from .constants import (
    CRITICAL,
    HIGH,
    MEDIUM,
    LOW,
    INFO,
    UNKNOWN,
)


# ==========================================================
# Empty Statistics
# ==========================================================

def empty_statistics() -> dict:
    """
    Return empty statistics.
    """

    return {
        "total_targets": 0,
        "total_findings": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0,
        "unknown": 0,
        "severity_statistics": {},
        "template_statistics": {},
        "target_statistics": {},
        "protocol_statistics": {},
        "tag_statistics": {},
        "unique_templates": 0,
        "unique_targets": 0,
        "top_templates": [],
        "top_targets": [],
        "top_tags": [],
        "cve_count": 0,
        "average_findings_per_target": 0,
    }


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    findings: list[dict],
) -> dict:
    """
    Generate statistics from findings.
    """

    if not findings:
        return empty_statistics()

    severity = Counter()
    templates = Counter()
    targets = Counter()
    tags = Counter()
    protocols = Counter()

    cves = 0

    for finding in findings:

        sev = finding.get(
            "severity",
            INFO,
        ).lower()

        severity[sev] += 1

        template = finding.get(
            "template_id",
            "",
        )

        if template:
            templates[template] += 1

        target = finding.get(
            "target",
            "",
        )

        if target:
            targets[target] += 1

        protocol = finding.get(
            "protocol",
            "",
        )

        if protocol:
            protocols[protocol] += 1

        for tag in finding.get(
            "tags",
            [],
        ):
            tags[tag] += 1

        cves += len(
            finding.get(
                "cves",
                [],
            )
        )

    total = len(findings)

    average_findings_per_target = (
        round(
            total / len(targets),
            2,
        )
        if targets
        else 0
    )

    return {

        "total_targets": len(targets),

        "total_findings": total,

        "critical": severity.get(
            CRITICAL,
            0,
        ),

        "high": severity.get(
            HIGH,
            0,
        ),

        "medium": severity.get(
            MEDIUM,
            0,
        ),

        "low": severity.get(
            LOW,
            0,
        ),

        "info": severity.get(
            INFO,
            0,
        ),

        "unknown": severity.get(
            UNKNOWN,
            0,
        ),

        "severity_statistics": dict(
            severity,
        ),

        "template_statistics": dict(
            templates,
        ),

        "target_statistics": dict(
            targets,
        ),

        "protocol_statistics": dict(
            protocols,
        ),

        "tag_statistics": dict(
            tags,
        ),

        "unique_templates": len(
            templates,
        ),

        "unique_targets": len(
            targets,
        ),

        "top_templates": templates.most_common(
            10,
        ),

        "top_targets": targets.most_common(
            10,
        ),

        "top_tags": tags.most_common(
            10,
        ),

        "cve_count": cves,

        "average_findings_per_target": (
            average_findings_per_target
        ),

    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "empty_statistics",
    "generate_statistics",
]