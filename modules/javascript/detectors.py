"""
JavaScript Secret Detector

Detects secrets from JavaScript source code
using the configured regex database.
"""

from core.logger import (
    warning,
)

from modules.javascript.secrets import (
    SECRET_PATTERNS,
)

from modules.javascript.filters import (
    filter_findings,
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
):
    """
    Normalize regex matches.

    Returns:
        list
    """

    normalized = set()

    for match in matches:

        if isinstance(

            match,

            tuple,

        ):

            value = next(

                (

                    item.strip()

                    for item

                    in match

                    if item

                ),

                "",

            )

        else:

            value = str(

                match

            ).strip()

        if value:

            normalized.add(

                value

            )

    return sorted(

        normalized

    )


# ==========================================================
# Detect Pattern
# ==========================================================

def detect_pattern(
    content: str,
    pattern,
):
    """
    Detect one regex pattern.

    Returns:
        list
    """

    try:

        return normalize_matches(

            pattern.findall(

                content

            )

        )

    except Exception as error:

        warning(

            f"Regex failed: {error}"

        )

        return []


# ==========================================================
# Detect Secrets
# ==========================================================

def detect_secrets(
    content: str,
):
    """
    Detect every supported
    secret type.

    Returns:
        dict
    """

    findings = {}

    for secret_type, pattern in SECRET_PATTERNS.items():

        matches = detect_pattern(

            content,

            pattern,

        )

        if matches:

            findings[
                secret_type
            ] = matches

    return findings


# ==========================================================
# Statistics
# ==========================================================

def generate_statistics(
    findings,
):
    """
    Generate statistics.

    Returns:
        dict
    """

    return {

        "secret_types": len(

            findings

        ),

        "total_secrets": sum(

            len(values)

            for values

            in findings.values()

        ),

    }


# ==========================================================
# Secret Pipeline
# ==========================================================

def process_findings(
    content: str,
):
    """
    Secret detection pipeline.

        Regex
           ↓
        Normalize
           ↓
        False Positive Filter

    Returns:
        dict
    """

    findings = detect_secrets(

        content

    )

    findings = filter_findings(

        findings

    )

    return findings


# ==========================================================
# Scan Content
# ==========================================================

def scan_content(
    content: str,
):
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

        findings = process_findings(

            content

        )

    except Exception as error:

        warning(

            f"Secret detection failed: {error}"

        )

        return EMPTY_RESULT.copy()

    return {

        "findings": findings,

        "statistics": generate_statistics(

            findings

        ),

    }