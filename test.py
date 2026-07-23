from pprint import pprint

from modules.tls.manager import run_tls_analysis


HOSTS = [

    "google.com",

    "github.com",

    "cloudflare.com",

]


# ==========================================================
# Run TLS Analysis
# ==========================================================

results, statistics = run_tls_analysis(

    HOSTS

)


# ==========================================================
# Results
# ==========================================================

print()

print("=" * 80)

print("Results Dictionary")

print("=" * 80)

pprint(

    results

)


print()

print("=" * 80)

print("Statistics Dictionary")

print("=" * 80)

pprint(

    statistics

)