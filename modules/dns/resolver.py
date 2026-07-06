"""
DNS Resolver

Resolve A (IPv4) and AAAA (IPv6) records.
"""

from modules.dns.helpers import (
    resolve_record,
    show_lookup,
)


# ==========================================================
# Resolve IPv4 (A)
# ==========================================================

def resolve_a(domain: str) -> list[str]:
    """
    Resolve IPv4 addresses.

    Args:
        domain (str)

    Returns:
        list[str]
    """

    show_lookup(
        domain,
        "A",
    )

    records = resolve_record(
        domain,
        "A",
    )

    return sorted(
        set(records)
    )


# ==========================================================
# Resolve IPv6 (AAAA)
# ==========================================================

def resolve_aaaa(domain: str) -> list[str]:
    """
    Resolve IPv6 addresses.

    Args:
        domain (str)

    Returns:
        list[str]
    """

    show_lookup(
        domain,
        "AAAA",
    )

    records = resolve_record(
        domain,
        "AAAA",
    )

    return sorted(
        set(records)
    )


# ==========================================================
# Resolve Both
# ==========================================================

def resolve_ip_addresses(domain: str) -> dict:
    """
    Resolve both IPv4 and IPv6.

    Returns:
        dict
    """

    return {

        "A": resolve_a(domain),

        "AAAA": resolve_aaaa(domain),

    }
