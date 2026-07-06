from modules.ports.manager import (
    scan_hosts,
)

from modules.ports.exporter import (
    save_open_ports,
    save_port_results,
    export_port_json,
    export_open_ports_csv,
    show_summary,
)

hosts = [

    "google.com",

    "github.com",

    "openai.com",

]

results, failed, elapsed = scan_hosts(
    hosts
)

save_open_ports(results)

save_port_results(results)

export_port_json(results)

export_open_ports_csv(results)

show_summary(
    results,
    failed,
    elapsed,
)