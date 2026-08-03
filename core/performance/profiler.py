"""
Performance Profiler

Execution time profiling utilities.
"""

from __future__ import annotations

from time import perf_counter

# ==========================================================
# Performance Profiler
# ==========================================================


class PerformanceProfiler:
    """
    Measure execution time.
    """

    def __init__(self) -> None:

        self._start: float | None = None
        self._elapsed: float = 0.0

    # ------------------------------------------------------
    # Start
    # ------------------------------------------------------

    def start(self) -> None:
        """
        Start the timer.
        """

        self._start = perf_counter()

    # ------------------------------------------------------
    # Stop
    # ------------------------------------------------------

    def stop(self) -> float:
        """
        Stop the timer.

        Returns:
            Elapsed time in seconds.
        """

        if self._start is None:

            raise RuntimeError("Profiler has not been started.")

        self._elapsed = perf_counter() - self._start

        self._start = None

        return self._elapsed

    # ------------------------------------------------------
    # Reset
    # ------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the profiler.
        """

        self._start = None
        self._elapsed = 0.0

    # ------------------------------------------------------
    # Elapsed
    # ------------------------------------------------------

    @property
    def elapsed(self) -> float:
        """
        Return the last measured
        execution time.
        """

        return self._elapsed


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "PerformanceProfiler",
]
