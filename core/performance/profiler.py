from __future__ import annotations

from time import perf_counter


class PerformanceProfiler:


    def __init__(self) -> None:

        self._start: float | None = None
        self._elapsed: float = 0.0


    def start(self) -> None:


        self._start = perf_counter()


    def stop(self) -> float:


        if self._start is None:

            raise RuntimeError("Profiler has not been started.")

        self._elapsed = perf_counter() - self._start

        self._start = None

        return self._elapsed


    def reset(self) -> None:


        self._start = None
        self._elapsed = 0.0


    @property
    def elapsed(self) -> float:


        return self._elapsed


__all__ = [
    "PerformanceProfiler",
]
