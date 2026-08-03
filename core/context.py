#!/usr/bin/env python3

"""
Execution Context
"""

from __future__ import annotations

from typing import Any

from core.performance import PerformanceManager

Analysis = dict[str, Any]


class ExecutionContext:
    """
    Shared execution context for the Recon Automation Framework.

    Stores
    ------
    - Module analysis
    - Performance manager
    - DNS cache
    - Shared HTTP session
    - Shared thread pool
    - Runtime statistics
    """

    def __init__(self) -> None:

        # --------------------------------------------------
        # Module Analysis
        # --------------------------------------------------

        self._analysis: dict[str, Analysis] = {}

        # --------------------------------------------------
        # Performance
        # --------------------------------------------------

        self.performance = PerformanceManager()

        # --------------------------------------------------
        # DNS Cache
        # --------------------------------------------------

        self._dns_cache: dict[str, list[str]] = {}

        # --------------------------------------------------
        # Shared Objects
        # --------------------------------------------------

        self._http_session: Any = None
        self._thread_pool: Any = None

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        self._statistics: dict[str, Any] = {}

    # ======================================================
    # Analysis
    # ======================================================

    def set_analysis(
        self,
        module: str,
        analysis: Analysis,
    ) -> None:

        self._analysis[module] = analysis

    def get_analysis(
        self,
        module: str,
    ) -> Analysis:

        return self._analysis.get(module, {})

    def has_analysis(
        self,
        module: str,
    ) -> bool:

        return module in self._analysis

    def analysis(self) -> dict[str, Analysis]:

        return dict(self._analysis)

    # ======================================================
    # DNS Cache
    # ======================================================

    def set_dns_cache(
        self,
        host: str,
        addresses: list[str],
    ) -> None:

        self._dns_cache[host] = addresses

    def get_dns_cache(
        self,
        host: str,
    ) -> list[str]:

        return self._dns_cache.get(host, [])

    def has_dns_cache(
        self,
        host: str,
    ) -> bool:

        return host in self._dns_cache

    def dns_cache(self) -> dict[str, list[str]]:

        return dict(self._dns_cache)

    # ======================================================
    # HTTP Session
    # ======================================================

    def set_http_session(
        self,
        session: Any,
    ) -> None:

        self._http_session = session

    def get_http_session(self) -> Any:

        return self._http_session

    # ======================================================
    # Thread Pool
    # ======================================================

    def set_thread_pool(
        self,
        pool: Any,
    ) -> None:

        self._thread_pool = pool

    def get_thread_pool(self) -> Any:

        return self._thread_pool

    # ======================================================
    # Statistics
    # ======================================================

    def set_statistic(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._statistics[key] = value

    def get_statistic(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._statistics.get(key, default)

    def statistics(self) -> dict[str, Any]:

        return dict(self._statistics)

    # ======================================================
    # Utility
    # ======================================================

    def clear(self) -> None:

        self._analysis.clear()
        self._dns_cache.clear()
        self._statistics.clear()

        self.performance.reset()

    def to_dict(self) -> dict[str, Any]:

        return {
            "analysis": self.analysis(),
            "statistics": self.statistics(),
            "performance": self.performance.summary(),
        }


__all__ = [
    "ExecutionContext",
]
