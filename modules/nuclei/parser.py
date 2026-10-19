import json
from pathlib import Path


def read_jsonl(
    filepath: str | Path,
):


    path = Path(filepath)

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

                    findings.append(json.loads(line))

                except json.JSONDecodeError:

                    continue

    except Exception:

        return []

    return findings


def extract_info(
    finding: dict,
):


    return finding.get(
        "info",
        {},
    )


def extract_references(
    finding: dict,
):


    return extract_info(finding).get(
        "reference",
        [],
    )


def extract_tags(
    finding: dict,
):


    return extract_info(finding).get(
        "tags",
        [],
    )


def extract_classification(
    finding: dict,
):


    classification = extract_info(finding).get(
        "classification",
        {},
    )

    cves = classification.get(
        "cve-id",
        [],
    )

    if isinstance(
        cves,
        str,
    ):

        cves = [cves]

    cwes = classification.get(
        "cwe-id",
        [],
    )

    if isinstance(
        cwes,
        str,
    ):

        cwes = [cwes]

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


def extract_metadata(
    finding: dict,
):


    return finding.get(
        "meta",
        {},
    )


def normalize_finding(
    finding: dict,
):


    info = extract_info(finding)

    return {


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


        "tags": extract_tags(finding),
        "references": extract_references(finding),
        "classification": extract_classification(finding),
        "metadata": extract_metadata(finding),
    }


def parse_findings(
    findings: list[dict],
):


    parsed = []

    for finding in findings:

        parsed.append(normalize_finding(finding))

    return parsed


def parse_file(
    filepath: str | Path,
):


    raw_findings = read_jsonl(filepath)

    if not raw_findings:

        return None

    findings = parse_findings(raw_findings)

    return {
        "findings": findings,
    }


def parse_nuclei(
    filepath: str | Path,
):


    return parse_file(filepath)


def total_findings(
    parsed: dict | None,
):


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


    return total_findings(parsed) == 0


if __name__ == "__main__":

    sample = parse_nuclei("output.jsonl")

    if is_empty(sample):

        print("No findings.")

    else:

        print(f"Findings : {total_findings(sample)}")

        first = sample["findings"][0]

        print()

        print("First Finding")

        print("-" * 40)

        print(f"Target      : {first['target']}")

        print(f"URL         : {first['url']}")

        print(f"Severity    : {first['severity']}")

        print(f"Template ID : {first['template_id']}")

        print(f"Template    : {first['template_name']}")
