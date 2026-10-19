from __future__ import annotations


def generate_statistics(
    results: dict[str, dict],
    failed_hosts: list[str],
) -> dict:


    http_hosts = 0
    https_hosts = 0

    status_codes: dict[int, int] = {}

    total_response_time = 0.0

    for data in results.values():

        if data.get("scheme") == "http":

            http_hosts += 1

        elif data.get("scheme") == "https":

            https_hosts += 1

        status = data.get("status")

        if status is not None:

            status_codes[status] = (
                status_codes.get(
                    status,
                    0,
                )
                + 1
            )

        total_response_time += data.get(
            "response_time",
            0.0,
        )

    alive_hosts = len(results)

    average_response_time = (
        round(
            total_response_time / alive_hosts,
            3,
        )
        if alive_hosts
        else 0.0
    )

    return {
        "alive_hosts": alive_hosts,
        "dead_hosts": len(
            failed_hosts,
        ),
        "http_hosts": http_hosts,
        "https_hosts": https_hosts,
        "status_codes": dict(
            sorted(
                status_codes.items(),
            )
        ),
        "average_response_time": average_response_time,
    }


__all__ = [
    "generate_statistics",
]
