"""
Nuclei Statistics

Generates statistics from
Nuclei findings.
"""

from collections import Counter


# ==========================================================
# Generate Statistics
# ==========================================================

def generate(
    findings: list,
):
    """
    Generate scan statistics.

    Args:
        findings:
            Normalized findings.

    Returns:
        dict
    """

    severity = Counter()

    templates = Counter()

    targets = Counter()

    tags = Counter()

    protocols = Counter()

    cves = 0

    for finding in findings:

        sev = finding.get(
            "severity",
            "info",
        ).lower()

        severity[sev] += 1

        template = finding.get(
            "template_id",
            "",
        )

        if template:

            templates[
                template
            ] += 1

        target = finding.get(
            "target",
            "",
        )

        if target:

            targets[
                target
            ] += 1

        protocol = finding.get(
            "protocol",
            "",
        )

        if protocol:

            protocols[
                protocol
            ] += 1

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

    total = len(
        findings
    )

    average = (

        round(

            total / len(targets),

            2,

        )

        if targets

        else 0

    )

    return {

        "total_findings": total,

        "critical": severity.get(
            "critical",
            0,
        ),

        "high": severity.get(
            "high",
            0,
        ),

        "medium": severity.get(
            "medium",
            0,
        ),

        "low": severity.get(
            "low",
            0,
        ),

        "info": severity.get(
            "info",
            0,
        ),

        "unknown": severity.get(
            "unknown",
            0,
        ),

        "severity_distribution": dict(
            severity
        ),

        "templates": dict(
            templates
        ),

        "targets": dict(
            targets
        ),

        "tags": dict(
            tags
        ),

        "protocols": dict(
            protocols
        ),

        "unique_templates": len(
            templates
        ),

        "unique_targets": len(
            targets
        ),

        "top_templates":

            templates.most_common(
                10
            ),

        "top_targets":

            targets.most_common(
                10
            ),

        "top_tags":

            tags.most_common(
                10
            ),

        "cve_count": cves,

        "average_findings_per_target":

            average,

    }


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    sample = [

        {

            "target":

                "https://example.com",

            "severity":

                "high",

            "template_id":

                "git-config",

            "protocol":

                "http",

            "tags":

                [

                    "git",

                    "exposure",

                ],

            "cves": [],

        }

    ]

    from pprint import pprint

    pprint(

        generate(
            sample
        )

    )