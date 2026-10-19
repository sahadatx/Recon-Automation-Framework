from __future__ import annotations

from typing import Any


class Benchmark:


    def __init__(self) -> None:

        self.reset()


    def reset(self) -> None:


        self._execution_time = 0.0
        self._targets = 0
        self._modules = 0
        self._memory_peak = 0.0
        self._results: list[dict[str, Any]] = []


    def set_execution_time(
        self,
        seconds: float,
    ) -> None:


        self._execution_time = seconds


    def set_targets(
        self,
        count: int,
    ) -> None:


        self._targets = count


    def set_memory_peak(
        self,
        peak_mb: float,
    ) -> None:


        self._memory_peak = peak_mb


    def add_module(
        self,
        *,
        name: str,
        execution_time: float,
        memory_mb: float = 0.0,
    ) -> None:


        self._modules += 1

        self._results.append(
            {
                "name": name,
                "execution_time": execution_time,
                "memory_mb": memory_mb,
            }
        )


    def fastest_module(
        self,
    ) -> dict[str, Any] | None:

        if not self._results:

            return None

        return min(
            self._results,
            key=lambda item: item["execution_time"],
        )


    def slowest_module(
        self,
    ) -> dict[str, Any] | None:

        if not self._results:

            return None

        return max(
            self._results,
            key=lambda item: item["execution_time"],
        )


    @property
    def throughput(
        self,
    ) -> float:


        if self._execution_time <= 0:

            return 0.0

        return round(
            self._targets / self._execution_time,
            2,
        )


    def summary(
        self,
    ) -> dict[str, Any]:


        average = 0.0

        if self._results:

            average = sum(item["execution_time"] for item in self._results) / len(
                self._results
            )

        return {
            "execution_time": round(
                self._execution_time,
                3,
            ),
            "targets": self._targets,
            "modules": self._modules,
            "throughput": self.throughput,
            "memory_peak_mb": round(
                self._memory_peak,
                2,
            ),
            "average_module_time": round(
                average,
                3,
            ),
            "fastest_module": self.fastest_module(),
            "slowest_module": self.slowest_module(),
        }


    @property
    def results(
        self,
    ) -> list[dict[str, Any]]:


        return list(
            self._results,
        )


__all__ = [
    "Benchmark",
]
