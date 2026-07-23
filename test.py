"""
Test TLS Protocol Module
"""

from pprint import pprint

from modules.tls.protocols import (
    collect_protocols,
    protocol_summary,
)


def main():

    host = "google.com"

    result = collect_protocols(

        host,

    )

    print("=" * 70)
    print("TLS Protocol Analysis")
    print("=" * 70)

    if result["error"]:

        print("Error:", result["error"])
        return

    pprint(result)

    print()

    summary = protocol_summary(

        result,

    )

    print("=" * 70)
    print("Protocol Summary")
    print("=" * 70)

    pprint(summary)

    print()

    print(f"Highest Protocol : {summary['highest_protocol']}")
    print(f"Security         : {summary['security']}")

    print()

    print("Supported Protocols")

    for protocol in summary["supported_protocols"]:

        print(f"  ✔ {protocol}")

    print()

    print("=" * 70)
    print("PASS")
    print("=" * 70)


if __name__ == "__main__":

    main()