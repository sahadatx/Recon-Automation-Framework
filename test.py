"""
Test TLS Cipher Module
"""

from pprint import pprint

from modules.tls.ciphers import (
    collect_cipher,
    cipher_summary,
)


def main():

    host = "google.com"

    result = collect_cipher(

        host,

    )

    print("=" * 70)
    print("TLS Cipher Analysis")
    print("=" * 70)

    if result["error"]:

        print("Error:", result["error"])
        return

    pprint(result)

    print()

    summary = cipher_summary(

        result,

    )

    print("=" * 70)
    print("Cipher Summary")
    print("=" * 70)

    pprint(summary)

    print()

    print(f"Cipher            : {summary['cipher']}")
    print(f"Protocol          : {summary['protocol']}")
    print(f"Bits              : {summary['bits']}")
    print(f"Strength          : {summary['strength']}")
    print(f"Forward Secrecy   : {summary['forward_secrecy']}")
    print(f"AEAD              : {summary['aead']}")
    print(f"Weak Cipher       : {summary['weak']}")

    print()

    print("=" * 70)
    print("PASS")
    print("=" * 70)


if __name__ == "__main__":

    main()