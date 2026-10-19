DEFAULT_SEVERITIES = {
    "critical",
    "high",
    "medium",
    "low",
    "info",
}


def remove_duplicates(
    findings: list,
):


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

    return list(unique.values())


def filter_severity(
    findings: list,
    severities=None,
):


    if severities is None:

        severities = DEFAULT_SEVERITIES

    severities = {severity.lower() for severity in severities}

    return [
        finding
        for finding in findings
        if finding.get(
            "severity",
            "",
        ).lower()
        in severities
    ]


def filter_templates(
    findings: list,
    templates: list | None = None,
):


    if not templates:

        return findings

    templates = set(templates)

    return [
        finding
        for finding in findings
        if finding.get(
            "template_id",
            "",
        )
        in templates
    ]


def filter_tags(
    findings: list,
    tags: list | None = None,
):


    if not tags:

        return findings

    tags = {tag.lower() for tag in tags}

    filtered = []

    for finding in findings:

        finding_tags = {
            tag.lower()
            for tag in finding.get(
                "tags",
                [],
            )
        }

        if finding_tags.intersection(tags):

            filtered.append(finding)

    return filtered


def filter_cves(
    findings: list,
):


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

            filtered.append(finding)

    return filtered


def exclude_templates(
    findings: list,
    templates: list | None = None,
):


    if not templates:

        return findings

    templates = set(templates)

    return [
        finding
        for finding in findings
        if finding.get(
            "template_id",
            "",
        )
        not in templates
    ]


def exclude_tags(
    findings: list,
    tags: list | None = None,
):


    if not tags:

        return findings

    tags = {tag.lower() for tag in tags}

    filtered = []

    for finding in findings:

        finding_tags = {
            tag.lower()
            for tag in finding.get(
                "tags",
                [],
            )
        }

        if not finding_tags.intersection(tags):

            filtered.append(finding)

    return filtered


def remove_informational(
    findings: list,
):


    return [
        finding
        for finding in findings
        if finding.get(
            "severity",
            "",
        ).lower()
        != "info"
    ]


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


    findings = remove_duplicates(findings)


    findings = filter_severity(
        findings,
        severities,
    )


    findings = filter_templates(
        findings,
        templates,
    )

    findings = exclude_templates(
        findings,
        exclude_template_list,
    )


    findings = filter_tags(
        findings,
        tags,
    )

    findings = exclude_tags(
        findings,
        exclude_tag_list,
    )


    if cves_only:

        findings = filter_cves(findings)


    if remove_info:

        findings = remove_informational(findings)

    return findings


def count_findings(
    findings: list,
):


    return len(findings)


def has_findings(
    findings: list,
):


    return bool(findings)


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

    filtered = apply_filters(sample)

    print(f"Findings : {count_findings(filtered)}")
