"""
Port Scanner Statistics

Generate statistics for port scan results.
"""

from __future__ import annotations

# ==========================================================
# Generate Statistics
# ==========================================================


def generate_statistics(
    results: dict,
    failed_hosts: list[str],
) -> dict:
    """
    Generate statistics from port scan results.

    Args:
        results:
            Successful scan results.

        failed_hosts:
            Hosts without open ports.

    Returns:
        Statistics dictionary.
    """

    hosts_with_open_ports = len(results)

    hosts_without_open_ports = len(failed_hosts)

    hosts_scanned = hosts_with_open_ports + hosts_without_open_ports

    total_open_ports = 0

    service_counts: dict[str, int] = {}

    for ports in results.values():

        total_open_ports += len(ports)

        for port in ports:

            service = port.get(
                "service",
                "unknown",
            )

            service_counts[service] = (
                service_counts.get(
                    service,
                    0,
                )
                + 1
            )

    average_open_ports = (
        round(
            total_open_ports / hosts_with_open_ports,
            2,
        )
        if hosts_with_open_ports
        else 0.0
    )

    return {
        "hosts_scanned": hosts_scanned,
        "hosts_with_open_ports": (hosts_with_open_ports),
        "hosts_without_open_ports": (hosts_without_open_ports),
        "total_open_ports": (total_open_ports),
        "average_open_ports": (average_open_ports),
        "service_counts": dict(
            sorted(
                service_counts.items(),
            )
        ),
    }


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "generate_statistics",
]
