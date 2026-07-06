from pprint import pprint

from modules.dns.records import (
    resolve_all_records,
)

domain = "google.com"

results = resolve_all_records(domain)

pprint(results)
