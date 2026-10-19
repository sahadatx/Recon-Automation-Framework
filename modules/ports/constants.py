from __future__ import annotations

from pathlib import Path


PORT_OUTPUT_DIR = Path("output/ports")


RESULTS_TXT = PORT_OUTPUT_DIR / "results.txt"

RESULTS_JSON = PORT_OUTPUT_DIR / "results.json"

RESULTS_CSV = PORT_OUTPUT_DIR / "results.csv"

SUMMARY_TXT = PORT_OUTPUT_DIR / "summary.txt"

OPEN_PORTS_TXT = PORT_OUTPUT_DIR / "open_ports.txt"


__all__ = [
    "PORT_OUTPUT_DIR",
    "RESULTS_TXT",
    "RESULTS_JSON",
    "RESULTS_CSV",
    "SUMMARY_TXT",
    "OPEN_PORTS_TXT",
]
