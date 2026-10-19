from modules.dns.helpers import resolve_record, show_lookup


def resolve_a(domain: str) -> list[str]:


    show_lookup(
        domain,
        "A",
    )

    records = resolve_record(
        domain,
        "A",
    )

    return sorted(set(records))


def resolve_aaaa(domain: str) -> list[str]:


    show_lookup(
        domain,
        "AAAA",
    )

    records = resolve_record(
        domain,
        "AAAA",
    )

    return sorted(set(records))


def resolve_ip_addresses(domain: str) -> dict:


    return {
        "A": resolve_a(domain),
        "AAAA": resolve_aaaa(domain),
    }
