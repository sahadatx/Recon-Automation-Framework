"""
Port Scanner

Core scanning functions.
"""

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from config.config import (
    PORT_SCAN_WORKERS,
)

from modules.ports.common_ports import (
    COMMON_PORTS,
)

from modules.ports.helpers import (
    scan_port,
    show_scan,
)

# Future
# from modules.ports.banner import (
#     grab_banner,
# )


# ==========================================================
# Scan One Host
# ==========================================================

def scan_host(
    host: str,
    ports: list[int],
):
    """
    Scan selected TCP ports for one host.

    Args:
        host: Target hostname.
        ports: List of TCP ports.

    Returns:
        list[dict]
    """

    open_ports = []

    with ThreadPoolExecutor(
        max_workers=min(
            PORT_SCAN_WORKERS,
            len(ports),
        )
    ) as executor:

        futures = {

            executor.submit(
                scan_port,
                host,
                port,
            ): port

            for port in ports

        }

        for future in as_completed(
            futures
        ):

            port = futures[
                future
            ]

            try:

                show_scan(
                    host,
                    port,
                )

                result = future.result()

                if not result:
                    continue

                # ==========================================
                # Future Banner Grabbing
                # ==========================================

                # result["banner"] = grab_banner(
                #     host,
                #     port,
                # )

                open_ports.append(
                    result
                )

            except Exception:
                continue

    return sorted(
        open_ports,
        key=lambda item: item["port"],
    )


# ==========================================================
# Scan Common Ports
# ==========================================================

def scan_common_ports(
    host: str,
):
    """
    Scan predefined common TCP ports.

    Returns:
        list[dict]
    """

    return scan_host(
        host,
        COMMON_PORTS,
    )


# ==========================================================
# Scan Custom Ports
# ==========================================================

def scan_custom_ports(
    host: str,
    ports: list[int],
):
    """
    Scan custom TCP ports.

    Returns:
        list[dict]
    """

    ports = sorted(
        set(ports)
    )

    return scan_host(
        host,
        ports,
    )