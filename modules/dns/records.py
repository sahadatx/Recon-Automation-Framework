"""
DNS Records

Resolve common DNS records.

Author : Sahadat Hossain
Project : Recon Automation Framework
"""

from modules.dns.helpers import (
    resolve_record,
    show_lookup,
)

from modules.dns.resolver import (
    resolve_a,
    resolve_aaaa,
)


# ==========================================================
# Resolve MX
# ==========================================================

def resolve_mx(domain: str) -> list[str]:
    """
    Resolve MX records.
    """

    show_lookup(domain, "MX")

    return resolve_record(
        domain,
        "MX",
    )


# ==========================================================
# Resolve NS
# ==========================================================

def resolve_ns(domain: str) -> list[str]:
    """
    Resolve NS records.
    """

    show_lookup(domain, "NS")

    return resolve_record(
        domain,
        "NS",
    )


# ==========================================================
# Resolve TXT
# ==========================================================

def resolve_txt(domain: str) -> list[str]:
    """
    Resolve TXT records.
    """

    show_lookup(domain, "TXT")

    return resolve_record(
        domain,
        "TXT",
    )


# ==========================================================
# Resolve SOA
# ==========================================================

def resolve_soa(domain: str) -> list[str]:
    """
    Resolve SOA records.
    """

    show_lookup(domain, "SOA")

    return resolve_record(
        domain,
        "SOA",
    )


# ==========================================================
# Resolve CNAME
# ==========================================================

def resolve_cname(domain: str) -> list[str]:
    """
    Resolve CNAME records.
    """

    show_lookup(domain, "CNAME")

    return resolve_record(
        domain,
        "CNAME",
    )


# ==========================================================
# Resolve All DNS Records
# ==========================================================

def resolve_all_records(domain: str) -> dict:
    """
    Resolve all supported DNS records.
    """

    return {

        "A": resolve_a(domain),

        "AAAA": resolve_aaaa(domain),

        "MX": resolve_mx(domain),

        "NS": resolve_ns(domain),

        "TXT": resolve_txt(domain),

        "SOA": resolve_soa(domain),

        "CNAME": resolve_cname(domain),

    }
