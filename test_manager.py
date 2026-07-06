from pprint import pprint

from modules.http.manager import (
    probe_hosts,
)

hosts = [
    "google.com",
    "github.com",
    "openai.com",
    "example.invalid",
]

results, failed, elapsed = probe_hosts(
    hosts
)

print()

print("Alive")

pprint(results)

print()

print("Failed")

pprint(failed)

print()

print(elapsed)
