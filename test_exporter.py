from modules.http.manager import (
    probe_hosts,
)

from modules.http.exporter import (
    save_alive_hosts,
    save_http_results,
    export_http_json,
    show_summary,
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

save_alive_hosts(results)

save_http_results(results)

export_http_json(results)

show_summary(
    results,
    failed,
    elapsed,
)
