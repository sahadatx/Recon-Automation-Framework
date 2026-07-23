"""
Email Security Helpers

Reusable helper functions for
Email Security.
"""

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

# ==========================================================
# Default Result
# ==========================================================

EMPTY_EMAIL_RESULT = deepcopy(

    DEFAULT_ANALYSIS,

)

# ==========================================================
# Normalize Target
# ==========================================================

def normalize_target(
    target: str,
) -> str:
    """
    Normalize target.

    Returns:
        str
    """

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


# ==========================================================
# DNS Lookup
# ==========================================================

def resolve_record(
    target: str,
    record_type: str,
) -> list[str]:
    """
    Resolve DNS record.

    Returns:
        list[str]
    """

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

            for answer
            in
            answers

        ]

    except Exception:

        return []


# ==========================================================
# MX Records
# ==========================================================

def resolve_mx(
    target: str,
) -> list[str]:
    """
    Resolve MX records.

    Returns:
        list[str]
    """

    return resolve_record(

        target,

        MX_RECORD,

    )


# ==========================================================
# TXT Records
# ==========================================================

def resolve_txt(
    target: str,
) -> list[str]:
    """
    Resolve TXT records.

    Returns:
        list[str]
    """

    return resolve_record(

        target,

        TXT_RECORD,

    )


# ==========================================================
# DNSKEY Records
# ==========================================================

def resolve_dnskey(
    target: str,
) -> bool:
    """
    Resolve DNSKEY records.

    Returns:
        bool
    """

    return bool(

        resolve_record(

            target,

            DNSKEY_RECORD,

        )

    )


# ==========================================================
# Safe Lower
# ==========================================================

def safe_lower(
    value: Any,
) -> str:
    """
    Safely convert a value
    to lowercase string.

    Returns:
        str
    """

    if value is None:

        return ""

    return str(

        value,

    ).lower()



# ==========================================================
# SPF Record
# ==========================================================

def resolve_spf(
    target: str,
) -> tuple[
    bool,
    str,
]:
    """
    Resolve SPF record.

    Returns:
        tuple(
            enabled,
            record,
        )
    """

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


# ==========================================================
# DMARC Record
# ==========================================================

def resolve_dmarc(
    target: str,
) -> tuple[
    bool,
    str,
]:
    """
    Resolve DMARC record.

    Returns:
        tuple(
            enabled,
            record,
        )
    """

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


# ==========================================================
# DKIM Record
# ==========================================================

def resolve_dkim(
    target: str,
) -> tuple[
    bool,
    str,
]:
    """
    Resolve DKIM record.

    Returns:
        tuple(
            enabled,
            selector,
        )
    """

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


# ==========================================================
# MTA-STS Record
# ==========================================================

def resolve_mta_sts(
    target: str,
) -> bool:
    """
    Resolve MTA-STS record.

    Returns:
        bool
    """

    return bool(

        resolve_txt(

            f"{MTA_STS_PREFIX}.{target}",

        )

    )


# ==========================================================
# TLS-RPT Record
# ==========================================================

def resolve_tls_rpt(
    target: str,
) -> bool:
    """
    Resolve TLS-RPT record.

    Returns:
        bool
    """

    return bool(

        resolve_txt(

            f"{TLS_RPT_PREFIX}.{target}",

        )

    )


# ==========================================================
# BIMI Record
# ==========================================================

def resolve_bimi(
    target: str,
) -> bool:
    """
    Resolve BIMI record.

    Returns:
        bool
    """

    return bool(

        resolve_txt(

            f"{BIMI_PREFIX}.{target}",

        )

    )


# ==========================================================
# Create Result
# ==========================================================

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
    """
    Create populated
    email security
    result.

    Returns:
        dict
    """

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


# ==========================================================
# Export
# ==========================================================

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