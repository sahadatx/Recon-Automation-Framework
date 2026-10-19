from modules.dns.helpers import resolve_record, show_lookup
from modules.dns.resolver import resolve_a, resolve_aaaa


def resolve_mx(domain: str) -> list[str]:


    show_lookup(domain, "MX")

    return resolve_record(
        domain,
        "MX",
    )


def resolve_ns(domain: str) -> list[str]:


    show_lookup(domain, "NS")

    return resolve_record(
        domain,
        "NS",
    )


def resolve_txt(domain: str) -> list[str]:


    show_lookup(domain, "TXT")

    return resolve_record(
        domain,
        "TXT",
    )


def resolve_soa(domain: str) -> list[str]:


    show_lookup(domain, "SOA")

    return resolve_record(
        domain,
        "SOA",
    )


def resolve_cname(domain: str) -> list[str]:


    show_lookup(domain, "CNAME")

    return resolve_record(
        domain,
        "CNAME",
    )


def resolve_all_records(domain: str) -> dict:


    return {
        "A": resolve_a(domain),
        "AAAA": resolve_aaaa(domain),
        "MX": resolve_mx(domain),
        "NS": resolve_ns(domain),
        "TXT": resolve_txt(domain),
        "SOA": resolve_soa(domain),
        "CNAME": resolve_cname(domain),
    }
