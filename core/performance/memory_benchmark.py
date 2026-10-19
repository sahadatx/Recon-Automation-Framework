from __future__ import annotations

from typing import Any


class MemoryBenchmark:


    def __init__(self) -> None:

        self._results: list[dict[str, Any]] = []


    def add_result(
        self,
        name: str,
        snapshot: dict[str, float],
    ) -> None:


        self._results.append(
            {
                "name": name,
                "current_mb": snapshot.get(
                    "current_mb",
                    0.0,
                ),
                "peak_mb": snapshot.get(
                    "peak_mb",
                    0.0,
                ),
                "difference_mb": snapshot.get(
                    "difference_mb",
                    0.0,
                ),
            }
        )


    @property
    def results(
        self,
    ) -> list[dict[str, Any]]:


        return list(
            self._results,
        )


    def best_run(
        self,
    ) -> dict[str, Any] | None:


        if not self._results:

            return None

        return min(
            self._results,
            key=lambda item: item["peak_mb"],
        )


    def worst_run(
        self,
    ) -> dict[str, Any] | None:


        if not self._results:

            return None

        return max(
            self._results,
            key=lambda item: item["peak_mb"],
        )


    def summary(
        self,
    ) -> dict[str, Any]:


        if not self._results:

            return {
                "runs": 0,
                "average_current_mb": 0.0,
                "average_peak_mb": 0.0,
                "lowest_peak_mb": 0.0,
                "highest_peak_mb": 0.0,
            }

        current = [item["current_mb"] for item in self._results]

        peak = [item["peak_mb"] for item in self._results]

        return {
            "runs": len(
                self._results,
            ),
            "average_current_mb": round(
                sum(current) / len(current),
                2,
            ),
            "average_peak_mb": round(
                sum(peak) / len(peak),
                2,
            ),
            "lowest_peak_mb": round(
                min(peak),
                2,
            ),
            "highest_peak_mb": round(
                max(peak),
                2,
            ),
        }


    def compare(
        self,
        first: str,
        second: str,
    ) -> dict[str, float] | None:


        left = next(
            (item for item in self._results if item["name"] == first),
            None,
        )

        right = next(
            (item for item in self._results if item["name"] == second),
            None,
        )

        if left is None or right is None:

            return None

        return {
            "current_mb": round(
                right["current_mb"] - left["current_mb"],
                2,
            ),
            "peak_mb": round(
                right["peak_mb"] - left["peak_mb"],
                2,
            ),
            "difference_mb": round(
                right["difference_mb"] - left["difference_mb"],
                2,
            ),
        }


    def reset(
        self,
    ) -> None:


        self._results.clear()


__all__ = [
    "MemoryBenchmark",
]
