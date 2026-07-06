"""
DNS Helper Functions

Shared helper functions used by the DNS
Resolution module.
"""

import dns.exception
import dns.resolver

from config.config import (
    DNS_TIMEOUT,
    DNS_SERVERS,
)

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

    # Use configured public DNS servers
    resolver.nameservers = DNS_SERVERS

    resolver.timeout = DNS_TIMEOUT
    resolver.lifetime = DNS_TIMEOUT

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
        domain: Target domain or subdomain.
        record_type: DNS record type.

    Returns:
        List of resolved records.
    """

    resolver = create_resolver()

    try:

        answers = resolver.resolve(
            domain,
            record_type,
            raise_on_no_answer=False,
        )

        if answers.rrset is None:
            return []

        return sorted(
            {
                answer.to_text().strip()
                for answer in answers
            }
        )

    except dns.resolver.NXDOMAIN:

        warning(
            f"{domain} does not exist."
        )

    except dns.resolver.NoNameservers:

        warning(
            f"No nameservers available for {domain}."
        )

    except dns.exception.Timeout:

        warning(
            f"{record_type} lookup timed out for {domain}."
        )

    except Exception as error:

        warning(
            f"{record_type} lookup failed for {domain}: {error}"
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
