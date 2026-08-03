"""
DNS Helper Functions

Shared helper functions used by the DNS
Resolution module.
"""

from __future__ import annotations

import dns.exception
import dns.resolver

from config.config import DNS_LIFETIME, DNS_RETRIES, DNS_SERVERS, DNS_TIMEOUT
from core.logger import info, warning

# ==========================================================
# Create Resolver
# ==========================================================


def create_resolver() -> dns.resolver.Resolver:
    """
    Create and configure a DNS resolver.

    Returns:
        Configured DNS resolver.
    """

    resolver = dns.resolver.Resolver()

    resolver.cache = dns.resolver.Cache()

    resolver.nameservers = DNS_SERVERS

    resolver.timeout = DNS_TIMEOUT

    resolver.lifetime = DNS_LIFETIME

    return resolver


# ==========================================================
# Resolve Record
# ==========================================================


def resolve_record(
    domain: str,
    record_type: str,
) -> list[str]:
    """
    Resolve a DNS record.

    Args:
        domain: Target domain.
        record_type: DNS record type.

    Returns:
        Resolved DNS records.
    """

    resolver = create_resolver()

    for attempt in range(
        1,
        DNS_RETRIES + 2,
    ):

        try:

            answers = resolver.resolve(
                domain,
                record_type,
                raise_on_no_answer=False,
            )

            if answers.rrset is None:
                return []

            return sorted({answer.to_text().strip() for answer in answers})

        except dns.exception.Timeout:

            if attempt <= DNS_RETRIES:

                warning(
                    f"{record_type} lookup timeout "
                    f"({attempt}/{DNS_RETRIES + 1}) "
                    f"for {domain}. Retrying..."
                )

                continue

            warning(f"{record_type} lookup timed out " f"for {domain}.")

            return []

        except dns.resolver.NXDOMAIN:

            warning(f"{domain} does not exist.")

            return []

        except dns.resolver.NoNameservers:

            warning(f"No nameservers available " f"for {domain}.")

            return []

        except Exception as error:

            warning(f"{record_type} lookup failed " f"for {domain}: {error}")

            return []

    return []


# ==========================================================
# Show Lookup
# ==========================================================


def show_lookup(
    domain: str,
    record_type: str,
) -> None:
    """
    Display DNS lookup information.

    Args:
        domain: Target domain.
        record_type: DNS record type.
    """

    info(f"Resolving {record_type} " f"records for {domain}")


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "create_resolver",
    "resolve_record",
    "show_lookup",
]
