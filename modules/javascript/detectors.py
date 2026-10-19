from __future__ import annotations

from core.logger import warning
from modules.javascript.filters import filter_findings
from modules.javascript.secrets import SECRET_PATTERNS


EMPTY_RESULT = {
    "findings": {},
    "statistics": {
        "secret_types": 0,
        "total_secrets": 0,
    },
}


def normalize_matches(
    matches,
) -> list[str]:


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


def detect_pattern(
    content: str,
    pattern,
) -> list[str]:


    try:

        return normalize_matches(pattern.findall(content))

    except Exception as error:

        warning(f"Regex failed: {error}")

        return []


def detect_secrets(
    content: str,
) -> dict[str, list[str]]:


    findings: dict[str, list[str]] = {}

    for secret_type, pattern in SECRET_PATTERNS.items():

        matches = detect_pattern(
            content,
            pattern,
        )

        if matches:

            findings[secret_type] = matches

    return findings


def generate_statistics(
    findings: dict[str, list[str]],
) -> dict[str, int]:


    return {
        "secret_types": len(findings),
        "total_secrets": sum(len(values) for values in findings.values()),
    }


def process_findings(
    content: str,
) -> dict[str, list[str]]:


    findings = detect_secrets(content)

    return filter_findings(findings)


def scan_content(
    content: str,
) -> dict:


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


__all__ = [
    "EMPTY_RESULT",
    "normalize_matches",
    "detect_pattern",
    "detect_secrets",
    "generate_statistics",
    "process_findings",
    "scan_content",
]
