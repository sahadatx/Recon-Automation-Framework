"""
Memory Profiler

Memory usage profiling utilities.
"""

from __future__ import annotations

import os
import tracemalloc

try:
    import psutil

    HAS_PSUTIL = True

except ImportError:

    psutil = None
    HAS_PSUTIL = False

try:
    import resource

    HAS_RESOURCE = True

except ImportError:

    resource = None
    HAS_RESOURCE = False


# ==========================================================
# Memory Profiler
# ==========================================================


class MemoryProfiler:
    """
    Memory usage profiler.
    """

    def __init__(self) -> None:

        self._started = False

    # ------------------------------------------------------
    # Start
    # ------------------------------------------------------

    def start(self) -> None:
        """
        Start memory profiling.
        """

        if not tracemalloc.is_tracing():

            tracemalloc.start()

        self._started = True

    # ------------------------------------------------------
    # Stop
    # ------------------------------------------------------

    def stop(self) -> None:
        """
        Stop memory profiling.
        """

        if tracemalloc.is_tracing():

            tracemalloc.stop()

        self._started = False

    # ------------------------------------------------------
    # Current Memory
    # ------------------------------------------------------

    @staticmethod
    def current_memory() -> float:
        """
        Return current process memory usage (MB).
        """

        if HAS_PSUTIL:

            process = psutil.Process(
                os.getpid(),
            )

            return (
                process.memory_info().rss
                / 1024
                / 1024
            )

        if HAS_RESOURCE:

            usage = resource.getrusage(
                resource.RUSAGE_SELF,
            )

            memory = usage.ru_maxrss

            # Linux: KB
            # macOS: bytes

            if os.name == "posix":

                return memory / 1024

            return (
                memory
                / 1024
                / 1024
            )

        current, _ = tracemalloc.get_traced_memory()

        return (
            current
            / 1024
            / 1024
        )

    # ------------------------------------------------------
    # Peak Memory
    # ------------------------------------------------------

    @staticmethod
    def peak_memory() -> float:
        """
        Return peak memory usage (MB).
        """

        if tracemalloc.is_tracing():

            _, peak = tracemalloc.get_traced_memory()

            return (
                peak
                / 1024
                / 1024
            )

        return MemoryProfiler.current_memory()

    # ------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------

    def snapshot(self) -> dict[str, float]:
        """
        Return a memory snapshot.
        """

        return {
            "current_mb": round(
                self.current_memory(),
                2,
            ),
            "peak_mb": round(
                self.peak_memory(),
                2,
            ),
            "difference_mb": round(
                self.peak_memory()
                - self.current_memory(),
                2,
            ),
        }

    # ------------------------------------------------------
    # Reset
    # ------------------------------------------------------

    def reset(self) -> None:
        """
        Reset profiler state.
        """

        self.stop()

    # ------------------------------------------------------
    # Is Running
    # ------------------------------------------------------

    @property
    def is_running(self) -> bool:
        """
        Return profiler status.
        """

        return self._started


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MemoryProfiler",
]