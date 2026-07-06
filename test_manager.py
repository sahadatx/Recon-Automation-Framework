from modules.dns.manager import (
    resolve_subdomains,
    save_dns_results,
    export_dns_json,
    show_summary,
)

targets = [
    "google.com",
    "github.com",
    "openai.com",
]

results, failed, elapsed = resolve_subdomains(
    targets
)

save_dns_results(results)

export_dns_json(results)

show_summary(
    results,
    failed,
    elapsed,
)
