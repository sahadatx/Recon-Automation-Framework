"""
JavaScript Secret Detector

Detects secrets from JavaScript source code
using the configured regex database.
"""

from modules.javascript.secrets import (
    SECRET_PATTERNS,
)

# from modules.javascript.filters import (
#     filter_findings,
# )


# ==========================================================
# Normalize Matches
# ==========================================================

def normalize_matches(
    matches: list,
) -> list[str]:
    """
    Normalize regex matches.

    Args:
        matches:
            Raw regex matches.

    Returns:
        Sorted unique matches.
    """

    cleaned = set()

    for match in matches:

        # Regex with capture groups
        if isinstance(
            match,
            tuple,
        ):

            value = ""

            for item in match:

                if item:

                    value = item.strip()

                    break

        else:

            value = str(
                match
            ).strip()

        if not value:

            continue

        cleaned.add(
            value
        )

    return sorted(
        cleaned
    )


# ==========================================================
# Detect One Pattern
# ==========================================================

def detect_pattern(
    content: str,
    pattern,
) -> list[str]:
    """
    Detect one secret type.

    Args:
        content:
            JavaScript content.

        pattern:
            Compiled regex.

    Returns:
        Secret matches.
    """

    matches = pattern.findall(
        content
    )

    return normalize_matches(
        matches
    )


# ==========================================================
# Detect Secrets
# ==========================================================

def detect_secrets(
    content: str,
) -> dict:
    """
    Detect every supported secret.

    Args:
        content:
            JavaScript source.

    Returns:
        Dictionary of findings.
    """

    findings = {}

    for secret_name, pattern in SECRET_PATTERNS.items():

        matches = detect_pattern(

            content,

            pattern,

        )

        if matches:

            findings[
                secret_name
            ] = matches

    return findings


# ==========================================================
# Statistics
# ==========================================================

def generate_statistics(
    findings: dict,
) -> dict:
    """
    Generate summary statistics.

    Args:
        findings:
            Filtered findings.

    Returns:
        Statistics dictionary.
    """

    total = 0

    for values in findings.values():

        total += len(
            values
        )

    return {

        "secret_types": len(
            findings
        ),

        "total_secrets": total,

    }


# ==========================================================
# Scan Content
# ==========================================================

def scan_content(
    content: str,
) -> dict:
    """
    Scan JavaScript content.

    Workflow

        Detect Secrets
            ↓
        Remove False Positives
            ↓
        Generate Statistics

    Args:
        content:
            JavaScript source.

    Returns:
        Scan result.
    """

    if not content:

        return {

            "findings": {},

            "statistics": {

                "secret_types": 0,

                "total_secrets": 0,

            },

        }

    findings = detect_secrets(
        content
    )

    # findings = filter_findings(
    #     findings
    # )

    statistics = generate_statistics(
        findings
    )

    return {

        "findings": findings,

        "statistics": statistics,

    }