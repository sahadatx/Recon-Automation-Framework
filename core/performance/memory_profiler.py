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


class MemoryProfiler:


    def __init__(self) -> None:

        self._started = False


    def start(self) -> None:


        if not tracemalloc.is_tracing():

            tracemalloc.start()

        self._started = True


    def stop(self) -> None:


        if tracemalloc.is_tracing():

            tracemalloc.stop()

        self._started = False


    @staticmethod
    def current_memory() -> float:


        if HAS_PSUTIL:

            process = psutil.Process(
                os.getpid(),
            )

            return process.memory_info().rss / 1024 / 1024

        if HAS_RESOURCE:

            usage = resource.getrusage(
                resource.RUSAGE_SELF,
            )

            memory = usage.ru_maxrss


            if os.name == "posix":

                return memory / 1024

            return memory / 1024 / 1024

        current, _ = tracemalloc.get_traced_memory()

        return current / 1024 / 1024


    @staticmethod
    def peak_memory() -> float:


        if tracemalloc.is_tracing():

            _, peak = tracemalloc.get_traced_memory()

            return peak / 1024 / 1024

        return MemoryProfiler.current_memory()


    def snapshot(self) -> dict[str, float]:


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
                self.peak_memory() - self.current_memory(),
                2,
            ),
        }


    def reset(self) -> None:


        self.stop()


    @property
    def is_running(self) -> bool:


        return self._started


__all__ = [
    "MemoryProfiler",
]
