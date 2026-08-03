"""
JavaScript Secret Detector

Detects secrets from JavaScript source code
using the configured regex database.
"""

from __future__ import annotations

from core.logger import (
    warning,
)

from modules.javascript.filters import (
    filter_findings,
)

from modules.javascript.secrets import (
    SECRET_PATTERNS,
)

# ==========================================================
# Empty Result
# ==========================================================

EMPTY_RESULT = {
    "findings": {},
    "statistics": {
        "secret_types": 0,
        "total_secrets": 0,
    },
}


# ==========================================================
# Normalize Matches
# ==========================================================


def normalize_matches(
    matches,
) -> list[str]:
    """
    Normalize regex matches.

    Returns:
        list[str]
    """

    normalized: set[str] = set()

    for match in matches:

        if isinstance(
            match,
            tuple,
        ):

            value = next(
                (item.strip() for item in match if item),
                "",
            )

        else:

            value = str(match).strip()

        if value:

            normalized.add(value)

    return sorted(normalized)


# ==========================================================
# Detect Pattern
# ==========================================================


def detect_pattern(
    content: str,
    pattern,
) -> list[str]:
    """
    Detect one regex pattern.

    Returns:
        list[str]
    """

    try:

        return normalize_matches(pattern.findall(content))

    except Exception as error:

        warning(f"Regex failed: {error}")

        return []


# ==========================================================
# Detect Secrets
# ==========================================================


def detect_secrets(
    content: str,
) -> dict[str, list[str]]:
    """
    Detect every supported
    secret type.

    Returns:
        dict[str, list[str]]
    """

    findings: dict[str, list[str]] = {}

    for secret_type, pattern in SECRET_PATTERNS.items():

        matches = detect_pattern(
            content,
            pattern,
        )

        if matches:

            findings[secret_type] = matches

    return findings


# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    findings: dict[str, list[str]],
) -> dict[str, int]:
    """
    Generate secret detection statistics.

    Returns:
        dict[str, int]
    """

    return {
        "secret_types": len(findings),
        "total_secrets": sum(len(values) for values in findings.values()),
    }


# ==========================================================
# Process Findings
# ==========================================================


def process_findings(
    content: str,
) -> dict[str, list[str]]:
    """
    Secret detection pipeline.

        Regex
           ↓
        Normalize
           ↓
        False Positive Filter

    Returns:
        dict[str, list[str]]
    """

    findings = detect_secrets(content)

    return filter_findings(findings)


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
        Normalize
              ↓
        False Positive Filter
              ↓
        Statistics

    Returns:
        dict
    """

    if not content:

        return EMPTY_RESULT.copy()

    try:

        findings = process_findings(content)

    except Exception as error:

        warning(f"Secret detection failed: {error}")

        return EMPTY_RESULT.copy()

    return {
        "findings": findings,
        "statistics": generate_statistics(findings),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "EMPTY_RESULT",
    "normalize_matches",
    "detect_pattern",
    "detect_secrets",
    "generate_statistics",
    "process_findings",
    "scan_content",
]
