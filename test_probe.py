from pprint import pprint

from modules.http.probe import (
    probe_host,
)

result = probe_host(
    "google.com"
)

pprint(result)
