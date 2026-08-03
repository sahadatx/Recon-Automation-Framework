"""
Performance Package

Performance monitoring and benchmarking.
"""

from __future__ import annotations

from .benchmark import Benchmark
from .bottleneck import detect_bottlenecks
from .bottleneck import summary as bottleneck_summary
from .manager import PerformanceManager
from .memory_analyzer import analyze_memory
from .memory_analyzer import summary as memory_summary
from .memory_benchmark import MemoryBenchmark
from .memory_profiler import MemoryProfiler
from .memory_report import generate_markdown as generate_memory_markdown
from .memory_report import generate_report as generate_memory_report
from .performance_report import generate_markdown, generate_report, generate_text
from .profiler import PerformanceProfiler

__all__ = [
    # Profilers
    "PerformanceManager",
    "PerformanceProfiler",
    "MemoryProfiler",
    # Analysis
    "analyze_memory",
    "memory_summary",
    # Bottleneck
    "detect_bottlenecks",
    "bottleneck_summary",
    # Benchmarks
    "Benchmark",
    "MemoryBenchmark",
    # Memory Report
    "generate_memory_report",
    "generate_memory_markdown",
    # Performance Report
    "generate_report",
    "generate_markdown",
    "generate_text",
]
