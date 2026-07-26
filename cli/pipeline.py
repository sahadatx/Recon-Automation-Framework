"""
CLI Pipeline

Build the execution pipeline
for the Recon Automation Framework.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Pipeline Order
# ==========================================================

PIPELINE = (

    "passive",

    "dns",

    "http",

    "ports",

    "tech",

    "crawler",

    "javascript",

    "fuzzing",

    "screenshots",

    "vhost",

    "nuclei",

    "waf",

    "tls",

    "cdn",

    "takeover",

    "email",

    "report",

    "dashboard",

)


# ==========================================================
# Module Dependencies
# ==========================================================

DEPENDENCIES: dict[str, tuple[str, ...]] = {

    "passive": (),

    "dns": (
        "passive",
    ),

    "http": (
        "dns",
    ),

    "ports": (
        "http",
    ),

    "tech": (
        "http",
    ),

    "crawler": (
        "http",
    ),

    "javascript": (
        "crawler",
    ),

    "fuzzing": (
        "http",
    ),

    "screenshots": (
        "http",
    ),

    "vhost": (
        "http",
    ),

    "nuclei": (
        "http",
    ),

    "waf": (
        "http",
    ),

    "tls": (
        "http",
    ),

    "cdn": (
        "http",
    ),

    "takeover": (
        "http",
    ),

    "email": (
        "http",
    ),

    "report": (

        "passive",

        "dns",

        "http",

        "ports",

        "tech",

        "crawler",

        "javascript",

        "fuzzing",

        "screenshots",

        "vhost",

        "nuclei",

        "waf",

        "tls",

        "cdn",

        "takeover",

        "email",

    ),

    "dashboard": (
        "report",
    ),

}


# ==========================================================
# Resolve Dependencies
# ==========================================================

def _resolve_dependencies(
    module: str,
    selected: set[str],
) -> None:
    """
    Resolve dependencies recursively.
    """

    for dependency in DEPENDENCIES.get(
        module,
        (),
    ):

        if dependency not in selected:

            _resolve_dependencies(
                dependency,
                selected,
            )

    selected.add(
        module,
    )


# ==========================================================
# Build Pipeline
# ==========================================================

def build_pipeline(
    config: dict[str, Any],
) -> list[str]:
    """
    Build the ordered execution pipeline.
    """

    selected: set[str] = set()

    modules = config[
        "modules"
    ]

    for module in PIPELINE:

        if not modules.get(
            module,
            False,
        ):

            continue

        _resolve_dependencies(
            module,
            selected,
        )

    pipeline: list[str] = []

    for module in PIPELINE:

        if module in selected:

            pipeline.append(
                module,
            )

    return pipeline


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "PIPELINE",

    "DEPENDENCIES",

    "build_pipeline",

]