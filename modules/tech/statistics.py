from __future__ import annotations


def generate_statistics(
    results: dict,
    failed_hosts: list[str],
) -> dict:


    hosts_analyzed = len(results) + len(failed_hosts)

    technology_counts: dict[
        str,
        int,
    ] = {}

    security_header_counts: dict[
        str,
        int,
    ] = {}

    technology_count = 0

    security_header_count = 0

    for data in results.values():

        technologies = data.get(
            "technologies",
            [],
        )

        security_headers = data.get(
            "security_headers",
            [],
        )

        technology_count += len(technologies)

        security_header_count += len(security_headers)

        for technology in technologies:

            technology_counts[technology] = (
                technology_counts.get(
                    technology,
                    0,
                )
                + 1
            )

        for header in security_headers:

            security_header_counts[header] = (
                security_header_counts.get(
                    header,
                    0,
                )
                + 1
            )

    return {
        "hosts_analyzed": (hosts_analyzed),
        "failed_hosts": len(failed_hosts),
        "technology_count": (technology_count),
        "security_header_count": (security_header_count),
        "technology_counts": dict(
            sorted(
                technology_counts.items(),
                key=lambda item: (
                    item[1],
                    item[0],
                ),
                reverse=True,
            )
        ),
        "security_header_counts": dict(
            sorted(
                security_header_counts.items(),
                key=lambda item: (
                    item[1],
                    item[0],
                ),
                reverse=True,
            )
        ),
    }


__all__ = [
    "generate_statistics",
]
