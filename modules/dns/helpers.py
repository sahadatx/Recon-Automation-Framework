"""
DNS Helper Functions

Shared helper functions used by the DNS
Resolution module.
"""

import dns.exception
import dns.resolver

from config.config import (
    DNS_TIMEOUT,
    DNS_LIFETIME,
    DNS_RETRIES,
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
    Create and configure a DNS resolver.

    Returns:
        dns.resolver.Resolver
    """

    resolver = dns.resolver.Resolver()

    # ------------------------------------------
    # Enable DNS Cache
    # ------------------------------------------

    resolver.cache = dns.resolver.Cache()

    # ------------------------------------------
    # Public DNS Servers
    # ------------------------------------------

    resolver.nameservers = DNS_SERVERS

    # ------------------------------------------
    # Timeout Configuration
    # ------------------------------------------

    resolver.timeout = DNS_TIMEOUT

    resolver.lifetime = DNS_LIFETIME

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

    Args:
        domain: Target domain/subdomain.
        record_type: DNS record type.

    Returns:
        list[str]
    """

    resolver = create_resolver()

    # ------------------------------------------
    # Retry Loop
    # ------------------------------------------

    for attempt in range(DNS_RETRIES + 1):

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

        except dns.exception.Timeout:

            if attempt < DNS_RETRIES:

                warning(
                    f"{record_type} lookup timeout "
                    f"({attempt + 1}/{DNS_RETRIES + 1}) "
                    f"for {domain}. Retrying..."
                )

                continue

            warning(
                f"{record_type} lookup timed out for {domain}"
            )

            return []

        except dns.resolver.NXDOMAIN:

            warning(
                f"{domain} does not exist."
            )

            return []

        except dns.resolver.NoNameservers:

            warning(
                f"No nameservers available for {domain}."
            )

            return []

        except Exception as error:

            warning(
                f"{record_type} lookup failed for "
                f"{domain}: {error}"
            )

            return []

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