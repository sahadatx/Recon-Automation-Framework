from __future__ import annotations

from concurrent.futures import as_completed
from typing import Any

from core.context import ExecutionContext
from modules.ports.common_ports import COMMON_PORTS
from modules.ports.helpers import scan_port, show_scan


def scan_host(
    context: ExecutionContext,
    host: str,
    ports: list[int],
) -> list[dict[str, Any]]:


    executor = context.get_thread_pool()

    if executor is None:
        raise RuntimeError("Shared thread pool is not initialized.")

    open_ports: list[dict[str, Any]] = []

    futures = {
        executor.submit(
            scan_port,
            host,
            port,
        ): port
        for port in ports
    }

    for future in as_completed(
        futures,
    ):

        port = futures[future]

        show_scan(
            host,
            port,
        )

        try:

            result = future.result()

        except Exception:
            continue

        if result is None:
            continue


        open_ports.append(
            result,
        )

    return sorted(
        open_ports,
        key=lambda item: item["port"],
    )


def scan_common_ports(
    context: ExecutionContext,
    host: str,
) -> list[dict[str, Any]]:


    return scan_host(
        context,
        host,
        COMMON_PORTS,
    )


def scan_custom_ports(
    context: ExecutionContext,
    host: str,
    ports: list[int],
) -> list[dict[str, Any]]:


    return scan_host(
        context,
        host,
        sorted(
            set(
                ports,
            ),
        ),
    )


__all__ = [
    "scan_host",
    "scan_common_ports",
    "scan_custom_ports",
]
