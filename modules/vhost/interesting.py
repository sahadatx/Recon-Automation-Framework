"""
Virtual Host Discovery

Detect interesting
virtual hosts.
"""


# ==========================================================
# Interesting Keywords
# ==========================================================

INTERESTING_KEYWORDS = {

    "admin",

    "api",

    "auth",

    "backup",

    "beta",

    "cdn",

    "dashboard",

    "db",

    "demo",

    "dev",

    "docs",

    "git",

    "gitlab",

    "grafana",

    "internal",

    "jenkins",

    "jira",

    "kibana",

    "mail",

    "monitor",

    "panel",

    "portal",

    "preview",

    "prod",

    "qa",

    "secure",

    "security",

    "soa",

    "sso",

    "stage",

    "staging",

    "status",

    "storage",

    "support",

    "test",

    "uat",

    "vpn",

    "webadmin",

    "webmail",

}


# ==========================================================
# Interesting Host
# ==========================================================

def is_interesting(
    host: str,
) -> bool:
    """
    Check whether host
    is interesting.

    Args:
        host:
            Virtual host.

    Returns:
        bool
    """

    host = host.lower()

    return any(

        keyword in host

        for keyword in INTERESTING_KEYWORDS

    )


# ==========================================================
# Scan Results
# ==========================================================

def scan(
    results: list,
) -> list:
    """
    Scan results and return
    interesting hosts.

    Args:
        results:
            Parsed results.

    Returns:
        list
    """

    interesting = []

    for result in results:

        host = result.get(

            "host",

            "",

        )

        if is_interesting(

            host

        ):

            interesting.append(

                result

            )

    return interesting


# ==========================================================
# Count Interesting Hosts
# ==========================================================

def count(
    results: list,
) -> int:
    """
    Count interesting hosts.

    Args:
        results:
            Parsed results.

    Returns:
        int
    """

    return len(

        scan(

            results

        )

    )