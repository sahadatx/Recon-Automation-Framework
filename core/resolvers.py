#!/usr/bin/env python3

"""
Module Input Resolvers
"""

from __future__ import annotations

from typing import Any
from typing import Callable

from core.context import ExecutionContext

Analysis = dict[str, Any]

Resolver = Callable[
    [ExecutionContext],
    tuple[Any, ...],
]


# ==========================================================
# Helpers
# ==========================================================


def _http_results(
    context: ExecutionContext,
) -> Analysis:
    """
    Return HTTP analysis results.
    """

    http = context.get_analysis(
        "http",
    )

    return http.get(
        "results",
        {},
    )


def _live_urls(
    context: ExecutionContext,
) -> list[str]:
    """
    Return all live URLs.
    """

    return sorted(
        {
            result["url"]
            for result in _http_results(
                context,
            ).values()
            if result.get(
                "url",
            )
        }
    )


# ==========================================================
# Resolver Functions
# ==========================================================


def resolve_dns(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    Passive → DNS
    """

    passive = context.get_analysis(
        "passive",
    )

    return (
        passive.get(
            "results",
            [],
        ),
    )


def resolve_http(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    DNS → HTTP
    """

    dns = context.get_analysis(
        "dns",
    )

    return (
        list(
            dns.get(
                "results",
                {},
            ).keys()
        ),
    )


def resolve_ports(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    HTTP → Ports
    """

    return (
        list(
            _http_results(
                context,
            ).keys()
        ),
    )


def resolve_tech(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    HTTP → Technology Detection
    """

    return (
        _http_results(
            context,
        ),
    )


def resolve_live_urls(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    HTTP → Live URL list
    """

    return (
        _live_urls(
            context,
        ),
    )


def resolve_javascript(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    Crawler → JavaScript URLs
    """

    crawler = context.get_analysis(
        "crawler",
    )

    javascript_urls = sorted(
        {
            script
            for host in crawler.get(
                "results",
                {},
            ).values()
            for page in host.get(
                "pages",
                {},
            ).values()
            for script in page.get(
                "parsed",
                {},
            ).get(
                "javascript",
                [],
            )
        }
    )

    return (javascript_urls,)


def resolve_screenshots(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    HTTP → Screenshot module
    """

    return (
        _http_results(
            context,
        ),
    )


def resolve_report(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    All analyses → Report
    """

    return (context.to_dict(),)


def resolve_dashboard(
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    Dashboard takes no arguments.
    """

    return ()


# ==========================================================
# Resolver Registry
# ==========================================================


RESOLVERS: dict[str, Resolver] = {
    "dns": resolve_dns,
    "http": resolve_http,
    "ports": resolve_ports,
    "tech": resolve_tech,
    "crawler": resolve_live_urls,
    "fuzzing": resolve_live_urls,
    "vhost": resolve_live_urls,
    "nuclei": resolve_live_urls,
    "waf": resolve_live_urls,
    "tls": resolve_live_urls,
    "cdn": resolve_live_urls,
    "takeover": resolve_live_urls,
    "email": resolve_live_urls,
    "javascript": resolve_javascript,
    "screenshots": resolve_screenshots,
    "report": resolve_report,
    "dashboard": resolve_dashboard,
}


def resolve_inputs(
    module: str,
    context: ExecutionContext,
) -> tuple[Any, ...]:
    """
    Resolve input arguments for a module.
    """

    try:
        resolver = RESOLVERS[module]

    except KeyError as error:

        raise ValueError(f"Unknown module: {module}") from error

    return resolver(
        context,
    )


def resolved_modules() -> set[str]:
    """
    Return all modules that have resolvers.
    """

    return set(
        RESOLVERS.keys(),
    )
