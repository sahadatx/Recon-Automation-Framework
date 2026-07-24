"""
Directory Fuzzing Test
"""

from __future__ import annotations

from modules.fuzzing.manager import (
    run_fuzzing,
)

from modules.fuzzing.exporter import (
    export_all,
)


def main() -> None:
    """
    Test Directory Fuzzing module.
    """

    targets = [

        "https://kubernetes.io",

        # "https://scanme.nmap.org",

    ]

    analysis = run_fuzzing(
        targets,
    )

    export_all(
        analysis,
    )


if __name__ == "__main__":

    main()