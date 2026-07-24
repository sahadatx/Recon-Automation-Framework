"""
DNS Resolution Statistics

Generate statistics for DNS resolution results.
"""

from __future__ import annotations


# ==========================================================
# Generate Statistics
# ==========================================================

def generate_statistics(
    results: dict[str, dict[str, list[str]]],
    failed_hosts: list[str],
) -> dict:
    """
    Generate DNS resolution statistics.

    Args:
        results: DNS resolution results.
        failed_hosts: Hosts that failed to resolve.

    Returns:
        DNS statistics.
    """

    record_types = (
        "A",
        "AAAA",
        "MX",
        "NS",
        "TXT",
        "SOA",
        "CNAME",
    )

    record_counts = {
        record_type: 0
        for record_type in record_types
    }

    enabled_hosts = {
        record_type: 0
        for record_type in record_types
    }

    for records in results.values():

        for record_type in record_types:

            values = records.get(
                record_type,
                [],
            )

            record_counts[
                record_type
            ] += len(values)

            if values:

                enabled_hosts[
                    record_type
                ] += 1

    total_records = sum(
        record_counts.values()
    )

    return {
        "resolved_hosts": len(
            results
        ),
        "failed_hosts": len(
            failed_hosts
        ),
        "total_records": total_records,
        "record_counts": record_counts,
        "enabled_hosts": enabled_hosts,
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
]