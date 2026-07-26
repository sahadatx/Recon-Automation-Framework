#!/usr/bin/env python3

"""
Module Registry
"""

from __future__ import annotations

from typing import Any
from typing import Callable

from modules.cdn.manager import run as run_cdn
from modules.crawler.manager import run as run_crawler
from modules.dashboard.manager import run as run_dashboard
from modules.dns.manager import run as run_dns
from modules.email.manager import run as run_email
from modules.fuzzing.manager import run as run_fuzzing
from modules.http.manager import run as run_http
from modules.javascript.manager import run as run_javascript
from modules.nuclei.manager import run as run_nuclei
from modules.passive.manager import run as run_passive
from modules.ports.manager import run as run_ports
from modules.report.manager import run as run_report
from modules.screenshots.manager import run as run_screenshots
from modules.takeover.manager import run as run_takeover
from modules.tech.manager import run as run_tech
from modules.tls.manager import run as run_tls
from modules.vhost.manager import run as run_vhost
from modules.waf.manager import run as run_waf


Runner = Callable[..., dict[str, Any]]


RUNNERS: dict[str, Runner] = {
    "passive": run_passive,
    "dns": run_dns,
    "http": run_http,
    "ports": run_ports,
    "tech": run_tech,
    "crawler": run_crawler,
    "javascript": run_javascript,
    "fuzzing": run_fuzzing,
    "screenshots": run_screenshots,
    "vhost": run_vhost,
    "nuclei": run_nuclei,
    "waf": run_waf,
    "tls": run_tls,
    "cdn": run_cdn,
    "takeover": run_takeover,
    "email": run_email,
    "report": run_report,
    "dashboard": run_dashboard,
}


def get_runner(
    module: str,
) -> Runner:
    """
    Return the registered runner.
    """

    try:
        return RUNNERS[module]

    except KeyError as error:
        raise ValueError(
            f"Unknown module: {module}"
        ) from error


def registered_modules() -> set[str]:
    """
    Return all registered module names.
    """

    return set(
        RUNNERS.keys(),
    )