from __future__ import annotations

import argparse
from typing import Any

from .parser import MODULES
from .validation import (
    validate_retries,
    validate_target,
    validate_threads,
    validate_timeout,
)


def build_config(
    arguments: argparse.Namespace,
) -> dict[str, Any]:


    modules = {
        module: (
            arguments.all
            or getattr(
                arguments,
                module,
            )
        )
        for module in MODULES
    }

    return {
        "target": validate_target(
            arguments.target,
        ),
        "threads": validate_threads(
            arguments.threads,
        ),
        "timeout": validate_timeout(
            arguments.timeout,
        ),
        "retries": validate_retries(
            arguments.retries,
        ),
        "verbose": arguments.verbose,
        "quiet": arguments.quiet,
        "modules": modules,
    }


__all__ = [
    "build_config",
]
