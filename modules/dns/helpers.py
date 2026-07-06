"""
DNS Helper Functions

Shared helper functions used by the DNS
Resolution module.
"""

import dns.exception
import dns.resolver

from config.config import DNS_TIMEOUT

from core.logger import (
    info,
    warning,
)


# ==========================================================
# Create Resolver
# ==========================================================

def create_resolver():
    """
    Create a configured DNS resolver.
    """

    resolver = dns.resolver.Resolver()

    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_TIMEOUT

    return resolver


# ==========================================================
# Resolve Record
# ==========================================================

def resolve_record(
    domain: str,
    record_type: str,
):
    """
    Resolve a DNS record.

    Returns:
        list[str]
    """

    resolver = create_resolver()

    try:

        answers = resolver.resolve(
            domain,
            record_type,
        )

        return sorted(
            {
                answer.to_text().strip()
                for answer in answers
            }
        )

    except dns.resolver.NoAnswer:

        warning(
            f"No {record_type} record found for {domain}"
        )

    except dns.resolver.NXDOMAIN:

        warning(
            f"{domain} does not exist"
        )

    except dns.resolver.NoNameservers:

        warning(
            f"No nameservers available for {domain}"
        )

    except dns.exception.Timeout:

        warning(
            f"{record_type} lookup timed out for {domain}"
        )

    except Exception as error:

        warning(
            f"{record_type} lookup failed: {error}"
        )

    return []


# ==========================================================
# Show Lookup
# ==========================================================

def show_lookup(
    domain: str,
    record_type: str,
):
    """
    Display lookup information.
    """

    info(
        f"Resolving {record_type} records for {domain}"
    )
