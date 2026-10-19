from __future__ import annotations

from copy import deepcopy
from typing import Any

import dns.resolver

from .constants import (
    BIMI_PREFIX,
    DEFAULT_ANALYSIS,
    DEFAULT_TIMEOUT,
    DKIM_SELECTORS,
    DMARC_PREFIX,
    DNSKEY_RECORD,
    MTA_STS_PREFIX,
    MX_RECORD,
    TLS_RPT_PREFIX,
    TXT_RECORD,
)


EMPTY_EMAIL_RESULT = deepcopy(
    DEFAULT_ANALYSIS,
)


def normalize_target(
    target: str,
) -> str:


    target = target.strip().lower()

    target = target.replace(
        "https://",
        "",
    )

    target = target.replace(
        "http://",
        "",
    )

    target = target.split(
        "/",
        1,
    )[0]

    return target


def resolve_record(
    target: str,
    record_type: str,
) -> list[str]:


    try:

        answers = dns.resolver.resolve(
            target,
            record_type,
            lifetime=DEFAULT_TIMEOUT,
        )

        return [
            str(
                answer,
            ).rstrip(".")
            for answer in answers
        ]

    except Exception:

        return []


def resolve_mx(
    target: str,
) -> list[str]:


    return resolve_record(
        target,
        MX_RECORD,
    )


def resolve_txt(
    target: str,
) -> list[str]:


    return resolve_record(
        target,
        TXT_RECORD,
    )


def resolve_dnskey(
    target: str,
) -> bool:


    return bool(
        resolve_record(
            target,
            DNSKEY_RECORD,
        )
    )


def safe_lower(
    value: Any,
) -> str:


    if value is None:

        return ""

    return str(
        value,
    ).lower()


def resolve_spf(
    target: str,
) -> tuple[
    bool,
    str,
]:


    for record in resolve_txt(
        target,
    ):

        if safe_lower(
            record,
        ).startswith(
            "v=spf1",
        ):

            return (
                True,
                record,
            )

    return (
        False,
        "",
    )


def resolve_dmarc(
    target: str,
) -> tuple[
    bool,
    str,
]:


    records = resolve_txt(
        f"{DMARC_PREFIX}.{target}",
    )

    if records:

        return (
            True,
            records[0],
        )

    return (
        False,
        "",
    )


def resolve_dkim(
    target: str,
) -> tuple[
    bool,
    str,
]:


    for selector in DKIM_SELECTORS:

        records = resolve_txt(
            f"{selector}._domainkey.{target}",
        )

        if records:

            return (
                True,
                selector,
            )

    return (
        False,
        "",
    )


def resolve_mta_sts(
    target: str,
) -> bool:


    return bool(
        resolve_txt(
            f"{MTA_STS_PREFIX}.{target}",
        )
    )


def resolve_tls_rpt(
    target: str,
) -> bool:


    return bool(
        resolve_txt(
            f"{TLS_RPT_PREFIX}.{target}",
        )
    )


def resolve_bimi(
    target: str,
) -> bool:


    return bool(
        resolve_txt(
            f"{BIMI_PREFIX}.{target}",
        )
    )


def create_result(
    target: str,
    mx: list[str],
    spf: bool,
    spf_record: str,
    dkim: bool,
    dkim_selector: str,
    dmarc: bool,
    dmarc_record: str,
    mta_sts: bool,
    tls_rpt: bool,
    bimi: bool,
    dnssec: bool,
) -> dict[str, Any]:


    result = deepcopy(
        EMPTY_EMAIL_RESULT,
    )

    result["target"] = target
    result["mx"] = mx
    result["spf"] = spf
    result["spf_record"] = spf_record
    result["dkim"] = dkim
    result["dkim_selector"] = dkim_selector
    result["dmarc"] = dmarc
    result["dmarc_record"] = dmarc_record
    result["mta_sts"] = mta_sts
    result["tls_rpt"] = tls_rpt
    result["bimi"] = bimi
    result["dnssec"] = dnssec

    return result


__all__ = [
    "EMPTY_EMAIL_RESULT",
    "normalize_target",
    "resolve_record",
    "resolve_mx",
    "resolve_txt",
    "resolve_dnskey",
    "safe_lower",
    "resolve_spf",
    "resolve_dmarc",
    "resolve_dkim",
    "resolve_mta_sts",
    "resolve_tls_rpt",
    "resolve_bimi",
    "create_result",
]
