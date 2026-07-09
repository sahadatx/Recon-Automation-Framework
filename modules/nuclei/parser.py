"""
Nuclei Parser

Parses Nuclei JSONL output into
normalized Python objects.
"""

import json

from pathlib import Path


# ==========================================================
# Read JSONL
# ==========================================================

def read_jsonl(
    filepath: str | Path,
):
    """
    Read Nuclei JSONL output.

    Args:
        filepath:
            JSONL output file.

    Returns:
        list
    """

    path = Path(
        filepath
    )

    if not path.exists():

        return []

    findings = []

    try:

        with path.open(

            "r",

            encoding="utf-8",

        ) as file:

            for line in file:

                line = line.strip()

                if not line:

                    continue

                try:

                    findings.append(

                        json.loads(
                            line
                        )

                    )

                except json.JSONDecodeError:

                    continue

    except Exception:

        return []

    return findings


# ==========================================================
# Extract Info
# ==========================================================

def extract_info(
    finding: dict,
):
    """
    Extract info section.

    Args:
        finding:
            Raw finding.

    Returns:
        dict
    """

    return finding.get(

        "info",

        {},

    )


# ==========================================================
# Extract References
# ==========================================================

def extract_references(
    finding: dict,
):
    """
    Extract references.

    Returns:
        list
    """

    return extract_info(

        finding

    ).get(

        "reference",

        [],

    )


# ==========================================================
# Extract Tags
# ==========================================================

def extract_tags(
    finding: dict,
):
    """
    Extract tags.

    Returns:
        list
    """

    return extract_info(

        finding

    ).get(

        "tags",

        [],

    )


# ==========================================================
# Extract Classification
# ==========================================================

def extract_classification(
    finding: dict,
):
    """
    Extract vulnerability
    classification.

    Returns:
        dict
    """

    classification = (

        extract_info(

            finding

        ).get(

            "classification",

            {},

        )

    )

    cves = classification.get(

        "cve-id",

        [],

    )

    if isinstance(

        cves,

        str,

    ):

        cves = [

            cves

        ]

    cwes = classification.get(

        "cwe-id",

        [],

    )

    if isinstance(

        cwes,

        str,

    ):

        cwes = [

            cwes

        ]

    return {

        "cves": cves,

        "cwes": cwes,

        "cvss": classification.get(

            "cvss-score",

            0,

        ),

        "cpe": classification.get(

            "cpe",

            [],

        ),

    }


# ==========================================================
# Extract Metadata
# ==========================================================

def extract_metadata(
    finding: dict,
):
    """
    Extract metadata.

    Returns:
        dict
    """

    return finding.get(

        "meta",

        {},

    )


# ==========================================================
# Normalize Finding
# ==========================================================

def normalize_finding(
    finding: dict,
):
    """
    Normalize one finding.

    Args:
        finding:
            Raw Nuclei finding.

    Returns:
        dict
    """

    info = extract_info(
        finding
    )

    return {

        # --------------------------------------------------
        # Target
        # --------------------------------------------------

        "target": finding.get(
            "host",
            "",
        ),

        "host": finding.get(
            "host",
            "",
        ),

        "url": finding.get(
            "matched-at",
            "",
        ),

        "scheme": finding.get(
            "scheme",
            "",
        ),

        "port": finding.get(
            "port",
            "",
        ),

        "ip": finding.get(
            "ip",
            "",
        ),

        "timestamp": finding.get(
            "timestamp",
            "",
        ),

        # --------------------------------------------------
        # Template
        # --------------------------------------------------

        "template_id": finding.get(
            "template-id",
            "",
        ),

        "template_name": info.get(
            "name",
            "",
        ),

        "template": finding.get(
            "template",
            "",
        ),

        # --------------------------------------------------
        # Finding
        # --------------------------------------------------

        "severity": info.get(
            "severity",
            "info",
        ),

        "description": info.get(
            "description",
            "",
        ),

        "matcher": finding.get(
            "matcher-name",
            "",
        ),

        "protocol": finding.get(
            "type",
            "",
        ),

        # --------------------------------------------------
        # Extra
        # --------------------------------------------------

        "tags": extract_tags(
            finding
        ),

        "references": extract_references(
            finding
        ),

        "classification": extract_classification(
            finding
        ),

        "metadata": extract_metadata(
            finding
        ),

    }


# ==========================================================
# Parse Findings
# ==========================================================

def parse_findings(
    findings: list[dict],
):
    """
    Normalize all findings.

    Args:
        findings:
            Raw findings.

    Returns:
        list
    """

    parsed = []

    for finding in findings:

        parsed.append(

            normalize_finding(
                finding
            )

        )

    return parsed


# ==========================================================
# Parse File
# ==========================================================

def parse_file(
    filepath: str | Path,
):
    """
    Parse Nuclei JSONL file.

    Args:
        filepath:
            JSONL output file.

    Returns:
        dict | None
    """

    raw_findings = read_jsonl(
        filepath
    )

    if not raw_findings:

        return None

    findings = parse_findings(
        raw_findings
    )

    return {

        "findings": findings,

    }


# ==========================================================
# Entry Point
# ==========================================================

def parse_nuclei(
    filepath: str | Path,
):
    """
    Parse Nuclei JSONL output.

    Args:
        filepath:
            JSONL file.

    Returns:
        dict | None
    """

    return parse_file(
        filepath
    )


# ==========================================================
# Helpers
# ==========================================================

def total_findings(
    parsed: dict | None,
):
    """
    Return total findings.

    Args:
        parsed:
            Parsed output.

    Returns:
        int
    """

    if parsed is None:

        return 0

    return len(

        parsed.get(

            "findings",

            [],

        )

    )


def is_empty(
    parsed: dict | None,
):
    """
    Check whether findings exist.

    Args:
        parsed:
            Parsed output.

    Returns:
        bool
    """

    return total_findings(
        parsed
    ) == 0


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    sample = parse_nuclei(
        "output.jsonl"
    )

    if is_empty(
        sample
    ):

        print(
            "No findings."
        )

    else:

        print(
            f"Findings : {total_findings(sample)}"
        )

        first = sample[
            "findings"
        ][0]

        print()

        print(
            "First Finding"
        )

        print(
            "-" * 40
        )

        print(
            f"Target      : {first['target']}"
        )

        print(
            f"URL         : {first['url']}"
        )

        print(
            f"Severity    : {first['severity']}"
        )

        print(
            f"Template ID : {first['template_id']}"
        )

        print(
            f"Template    : {first['template_name']}"
        )
