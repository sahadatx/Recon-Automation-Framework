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


def is_interesting(
    host: str,
) -> bool:


    host = host.lower()

    return any(keyword in host for keyword in INTERESTING_KEYWORDS)


def scan(
    results: list,
) -> list:


    interesting = []

    for result in results:

        host = result.get(
            "host",
            "",
        )

        if is_interesting(host):

            interesting.append(result)

    return interesting


def count(
    results: list,
) -> int:


    return len(scan(results))
