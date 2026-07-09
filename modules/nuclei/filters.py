"""
Nuclei Filters

Filters and normalizes
Nuclei findings.
"""

# ==========================================================
# Default Configuration
# ==========================================================

DEFAULT_SEVERITIES = {

    "critical",

    "high",

    "medium",

    "low",

    "info",

}

# ==========================================================
# Remove Duplicates
# ==========================================================

def remove_duplicates(
    findings: list,
):
    """
    Remove duplicate findings.

    Returns:
        list
    """

    unique = {}

    for finding in findings:

        key = (

            finding.get(
                "url",
                "",
            ),

            finding.get(
                "template_id",
                "",
            ),

        )

        unique[key] = finding

    return list(

        unique.values()

    )


# ==========================================================
# Filter Severity
# ==========================================================

def filter_severity(
    findings: list,
    severities=None,
):
    """
    Filter by severity.

    Returns:
        list
    """

    if severities is None:

        severities = DEFAULT_SEVERITIES

    severities = {

        severity.lower()

        for severity in severities

    }

    return [

        finding

        for finding in findings

        if finding.get(

            "severity",

            "",

        ).lower() in severities

    ]


# ==========================================================
# Filter Templates
# ==========================================================

def filter_templates(
    findings: list,
    templates: list | None = None,
):
    """
    Include only selected templates.

    Returns:
        list
    """

    if not templates:

        return findings

    templates = set(

        templates

    )

    return [

        finding

        for finding in findings

        if finding.get(

            "template_id",

            "",

        ) in templates

    ]

# ==========================================================
# Filter Tags
# ==========================================================

def filter_tags(
    findings: list,
    tags: list | None = None,
):
    """
    Include findings containing
    selected tags.

    Returns:
        list
    """

    if not tags:

        return findings

    tags = {

        tag.lower()

        for tag in tags

    }

    filtered = []

    for finding in findings:

        finding_tags = {

            tag.lower()

            for tag in finding.get(

                "tags",

                [],

            )

        }

        if finding_tags.intersection(

            tags

        ):

            filtered.append(

                finding

            )

    return filtered


# ==========================================================
# CVE Only
# ==========================================================

def filter_cves(
    findings: list,
):
    """
    Keep findings that contain
    at least one CVE.

    Returns:
        list
    """

    filtered = []

    for finding in findings:

        classification = finding.get(

            "classification",

            {},

        )

        cves = classification.get(

            "cves",

            [],

        )

        if cves:

            filtered.append(

                finding

            )

    return filtered


# ==========================================================
# Exclude Templates
# ==========================================================

def exclude_templates(
    findings: list,
    templates: list | None = None,
):
    """
    Exclude selected templates.

    Returns:
        list
    """

    if not templates:

        return findings

    templates = set(

        templates

    )

    return [

        finding

        for finding in findings

        if finding.get(

            "template_id",

            "",

        ) not in templates

    ]


# ==========================================================
# Exclude Tags
# ==========================================================

def exclude_tags(
    findings: list,
    tags: list | None = None,
):
    """
    Exclude findings containing
    selected tags.

    Returns:
        list
    """

    if not tags:

        return findings

    tags = {

        tag.lower()

        for tag in tags

    }

    filtered = []

    for finding in findings:

        finding_tags = {

            tag.lower()

            for tag in finding.get(

                "tags",

                [],

            )

        }

        if not finding_tags.intersection(

            tags

        ):

            filtered.append(

                finding

            )

    return filtered


# ==========================================================
# Remove Informational Findings
# ==========================================================

def remove_informational(
    findings: list,
):
    """
    Remove informational findings.

    Returns:
        list
    """

    return [

        finding

        for finding in findings

        if finding.get(

            "severity",

            "",

        ).lower() != "info"

    ]



# ==========================================================
# Apply Filters
# ==========================================================

def apply_filters(
    findings: list,
    severities=None,
    templates=None,
    tags=None,
    exclude_template_list=None,
    exclude_tag_list=None,
    cves_only: bool = False,
    remove_info: bool = False,
):
    """
    Apply filter pipeline.

    Args:
        findings:
            Parsed findings.

        severities:
            Allowed severities.

        templates:
            Included templates.

        tags:
            Included tags.

        exclude_template_list:
            Excluded templates.

        exclude_tag_list:
            Excluded tags.

        cves_only:
            Keep only CVE findings.

        remove_info:
            Remove informational findings.

    Returns:
        list
    """

    # ------------------------------------------------------
    # Remove Duplicates
    # ------------------------------------------------------

    findings = remove_duplicates(
        findings
    )

    # ------------------------------------------------------
    # Severity
    # ------------------------------------------------------

    findings = filter_severity(

        findings,

        severities,

    )

    # ------------------------------------------------------
    # Templates
    # ------------------------------------------------------

    findings = filter_templates(

        findings,

        templates,

    )

    findings = exclude_templates(

        findings,

        exclude_template_list,

    )

    # ------------------------------------------------------
    # Tags
    # ------------------------------------------------------

    findings = filter_tags(

        findings,

        tags,

    )

    findings = exclude_tags(

        findings,

        exclude_tag_list,

    )

    # ------------------------------------------------------
    # CVEs
    # ------------------------------------------------------

    if cves_only:

        findings = filter_cves(
            findings
        )

    # ------------------------------------------------------
    # Remove Info
    # ------------------------------------------------------

    if remove_info:

        findings = remove_informational(
            findings
        )

    return findings


# ==========================================================
# Helpers
# ==========================================================

def count_findings(
    findings: list,
):
    """
    Return total findings.

    Returns:
        int
    """

    return len(
        findings
    )


def has_findings(
    findings: list,
):
    """
    Check findings exist.

    Returns:
        bool
    """

    return bool(
        findings
    )


# ==========================================================
# Self Test
# ==========================================================

if __name__ == "__main__":

    sample = [

        {

            "url": "https://example.com",

            "template_id": "git-config",

            "severity": "high",

            "tags": [

                "git",

                "exposure",

            ],

            "classification": {

                "cves": [],

            },

        },

        {

            "url": "https://example.com",

            "template_id": "git-config",

            "severity": "high",

            "tags": [

                "git",

            ],

            "classification": {

                "cves": [],

            },

        },

    ]

    filtered = apply_filters(
        sample
    )

    print(
        f"Findings : {count_findings(filtered)}"
    )



