from __future__ import annotations

from typing import Any

from .benchmark import Benchmark
from .bottleneck import detect_bottlenecks
from .memory_analyzer import analyze_memory
from .memory_benchmark import MemoryBenchmark
from .memory_profiler import MemoryProfiler
from .performance_report import generate_markdown, generate_report, generate_text
from .profiler import PerformanceProfiler


class PerformanceManager:


    def __init__(self) -> None:

        self._framework_profiler = PerformanceProfiler()


        self._module_profilers: dict[
            str,
            PerformanceProfiler,
        ] = {}


        self._memory_profiler = MemoryProfiler()


        self._benchmark = Benchmark()
        self._memory_benchmark = MemoryBenchmark()


        self._memory_snapshot: dict[
            str,
            float,
        ] = {}

        self._memory_analysis: dict[
            str,
            Any,
        ] = {}

        self._benchmark_summary: dict[
            str,
            Any,
        ] = {}

        self._bottlenecks: list[dict[str, Any]] = []

        self._report: dict[
            str,
            Any,
        ] = {}

        self._running = False


    def start(self) -> None:


        if self._running:
            return

        self._framework_profiler.reset()
        self._framework_profiler.start()

        self._memory_profiler.reset()
        self._memory_profiler.start()

        self._benchmark.reset()
        self._memory_benchmark.reset()

        self._module_profilers.clear()

        self._memory_snapshot.clear()
        self._memory_analysis.clear()
        self._benchmark_summary.clear()
        self._bottlenecks.clear()
        self._report.clear()

        self._running = True

    def stop(self) -> float:


        if not self._running:
            return 0.0

        execution_time = self._framework_profiler.stop()

        self._memory_snapshot = self._memory_profiler.snapshot()

        self._memory_profiler.stop()

        self._benchmark.set_execution_time(execution_time)

        self._benchmark.set_memory_peak(
            self._memory_snapshot.get(
                "peak_mb",
                0.0,
            )
        )

        self._running = False

        return execution_time


    def start_module(
        self,
        module: str,
    ) -> None:


        profiler = PerformanceProfiler()

        profiler.start()

        self._module_profilers[module] = profiler

    def stop_module(
        self,
        module: str,
    ) -> float:


        profiler = self._module_profilers.get(
            module,
        )

        if profiler is None:
            raise RuntimeError(f"Module '{module}' " "has not been started.")

        elapsed = profiler.stop()

        snapshot = self._memory_profiler.snapshot()

        self._benchmark.add_module(
            name=module,
            execution_time=elapsed,
            memory_mb=snapshot.get(
                "peak_mb",
                0.0,
            ),
        )

        self._memory_benchmark.add_result(
            module,
            snapshot,
        )

        del self._module_profilers[module]

        return elapsed


    def set_target_count(
        self,
        count: int,
    ) -> None:


        self._benchmark.set_targets(count)

    @property
    def benchmark(
        self,
    ) -> Benchmark:


        return self._benchmark

    @property
    def memory_benchmark(
        self,
    ) -> MemoryBenchmark:


        return self._memory_benchmark

    @property
    def module_results(
        self,
    ) -> list[dict[str, Any]]:


        return self._benchmark.results

    @property
    def execution_time(
        self,
    ) -> float:


        return self._framework_profiler.elapsed


    @property
    def memory_snapshot(
        self,
    ) -> dict[str, float]:


        return dict(self._memory_snapshot)

    @property
    def memory_analysis(
        self,
    ) -> dict[str, Any]:


        return dict(self._memory_analysis)

    def analyze_memory(self) -> dict[str, Any]:


        if not self._memory_snapshot:
            self._memory_snapshot = self._memory_profiler.snapshot()

        self._memory_analysis = analyze_memory(
            self._memory_snapshot,
        )

        return self._memory_analysis


    def detect_bottlenecks(
        self,
    ) -> list[dict[str, Any]]:


        metrics = {
            "execution_time": (self.execution_time),
            "memory_peak_mb": (
                self._memory_snapshot.get(
                    "peak_mb",
                    0.0,
                )
            ),


            "cpu_percent": 0.0,
        }

        self._bottlenecks = detect_bottlenecks(metrics)

        return list(self._bottlenecks)

    @property
    def bottlenecks(
        self,
    ) -> list[dict[str, Any]]:


        return list(self._bottlenecks)


    def generate_report(
        self,
    ) -> dict[str, Any]:


        if not self._memory_analysis:
            self.analyze_memory()

        if not self._bottlenecks:
            self.detect_bottlenecks()

        self._benchmark_summary = self._memory_benchmark.summary()

        self._report = generate_report(
            execution_time=self.execution_time,
            memory=self._memory_analysis,
            bottlenecks=self._bottlenecks,
            benchmark=self._benchmark_summary,
        )

        return self._report

    @property
    def report(
        self,
    ) -> dict[str, Any]:


        if not self._report:
            return self.generate_report()

        return dict(self._report)


    def markdown(self) -> str:


        if not self._report:
            self.generate_report()

        return generate_markdown(
            self._report,
        )

    def text(self) -> str:


        if not self._report:
            self.generate_report()

        return generate_text(
            self._report,
        )

    def summary(
        self,
    ) -> dict[str, Any]:


        return {
            "execution_time": self.execution_time,
            "memory": self.memory_snapshot,
            "benchmark": self._benchmark.summary(),
            "memory_benchmark": (self._memory_benchmark.summary()),
            "bottlenecks": list(self._bottlenecks),
        }


    def reset(self) -> None:


        self._framework_profiler.reset()

        self._memory_profiler.reset()

        self._benchmark.reset()

        self._memory_benchmark.reset()

        self._module_profilers.clear()

        self._memory_snapshot.clear()

        self._memory_analysis.clear()

        self._benchmark_summary.clear()

        self._bottlenecks.clear()

        self._report.clear()

        self._running = False


    @property
    def is_running(
        self,
    ) -> bool:


        return self._running


__all__ = [
    "PerformanceManager",
]
