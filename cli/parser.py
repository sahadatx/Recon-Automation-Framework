"""
CLI Parser

Command-line interface parser
for the Recon Automation Framework.
"""

from __future__ import annotations

import argparse


# ==========================================================
# Framework Modules
# ==========================================================

MODULES = (

    "passive",

    "dns",

    "http",

    "ports",

    "crawler",

    "javascript",

    "fuzzing",

    "screenshots",

    "vhost",

    "tech",

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
# Create Parser
# ==========================================================

def create_parser() -> argparse.ArgumentParser:
    """
    Create the framework CLI parser.
    """

    parser = argparse.ArgumentParser(

        prog="recon",

        description=(
            "Recon Automation Framework\n"
            "Modular reconnaissance and "
            "security assessment toolkit."
        ),

        formatter_class=(
            argparse.ArgumentDefaultsHelpFormatter
        ),

    )

    # ------------------------------------------------------
    # Target
    # ------------------------------------------------------

    parser.add_argument(

        "target",

        metavar="TARGET",

        help=(
            "Target domain, hostname, "
            "or IP address."
        ),

    )

    # ------------------------------------------------------
    # Scan Options
    # ------------------------------------------------------

    scan = parser.add_argument_group(
        "Scan Options",
    )

    scan.add_argument(

        "--all",

        action="store_true",

        help="Run all framework modules.",

    )

    # ------------------------------------------------------
    # Module Options
    # ------------------------------------------------------

    modules = parser.add_argument_group(
        "Module Options",
    )

    for module in MODULES:

        modules.add_argument(

            f"--{module}",

            action="store_true",

            help=f"Run the {module} module.",

        )

    # ------------------------------------------------------
    # Performance
    # ------------------------------------------------------

    performance = parser.add_argument_group(
        "Performance",
    )

    performance.add_argument(

        "--threads",

        type=int,

        default=50,

        metavar="N",

        help="Worker thread count.",

    )

    performance.add_argument(

        "--timeout",

        type=int,

        default=10,

        metavar="SECONDS",

        help="Request timeout.",

    )

    performance.add_argument(

        "--retries",

        type=int,

        default=3,

        metavar="N",

        help="Retry attempts.",

    )

    # ------------------------------------------------------
    # Logging
    # ------------------------------------------------------

    logging = parser.add_argument_group(
        "Logging",
    )

    logging.add_argument(

        "-v",
        "--verbose",

        action="store_true",

        help="Enable verbose output.",

    )

    logging.add_argument(

        "-q",
        "--quiet",

        action="store_true",

        help="Suppress informational output.",

    )

    # ------------------------------------------------------
    # General
    # ------------------------------------------------------

    general = parser.add_argument_group(
        "General",
    )

    general.add_argument(

        "--version",

        action="version",

        version="Recon Automation Framework v1.0",

    )

    return parser


# ==========================================================
# Parse Arguments
# ==========================================================

def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = create_parser()

    return parser.parse_args()


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [

    "MODULES",

    "create_parser",

    "parse_arguments",

]