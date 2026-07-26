"""
Executor Test
"""

from __future__ import annotations

from core.executor import (
    execute_module,
    execute_pipeline,
)


def test_execute_module() -> None:
    """
    Test execute_module().
    """

    print("=" * 60)
    print("EXECUTE MODULE TEST")
    print("=" * 60)

    analysis = execute_module(
        "dashboard",
    )

    assert isinstance(
        analysis,
        dict,
    )

    print("[OK] dashboard executed")
    print()


def test_execute_pipeline() -> None:
    """
    Test execute_pipeline().
    """

    print("=" * 60)
    print("EXECUTE PIPELINE TEST")
    print("=" * 60)

    pipeline = [
        "dashboard",
        "report",
    ]

    results = execute_pipeline(
        pipeline,
    )

    assert isinstance(
        results,
        dict,
    )

    assert set(
        results.keys()
    ) == set(
        pipeline
    )

    for module in pipeline:

        assert isinstance(
            results[module],
            dict,
        )

        print(f"[OK] {module}")

    print()


def main() -> None:

    test_execute_module()

    test_execute_pipeline()

    print("=" * 60)
    print("ALL EXECUTOR TESTS PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()