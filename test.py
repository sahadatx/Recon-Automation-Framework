"""
Test TLS Certificate Module
"""

from pprint import pprint

from modules.tls.certificate import (
    collect_certificate,
)


def main():

    host = "google.com"

    result = collect_certificate(host)

    print("=" * 70)
    print("TLS Certificate Test")
    print("=" * 70)

    if result["error"]:

        print("Error:", result["error"])
        return

    print(f"Host                 : {result['host']}")
    print(f"Port                 : {result['port']}")
    print(f"TLS Version          : {result['tls_version']}")
    print(f"Cipher               : {result['cipher']}")

    print()

    print("Subject")
    pprint(result["subject"])

    print()

    print("Issuer")
    pprint(result["issuer"])

    print()

    print("Subject Alternative Names")

    for dns in result["san"]:

        print(f"  - {dns}")

    print()

    print(f"Serial Number        : {result['serial_number']}")
    print(f"Certificate Version  : {result['certificate_version']}")
    print(f"Signature Algorithm  : {result['signature_algorithm']}")
    print(f"Public Key Type      : {result['public_key_type']}")
    print(f"Public Key Size      : {result['public_key_size']} bits")

    print()

    print(f"Not Before           : {result['not_before']}")
    print(f"Not After            : {result['not_after']}")

    print()

    print("SHA1")
    print(result["sha1"])

    print()

    print("SHA256")
    print(result["sha256"])

    print()

    print("X509 Loaded          :", result["x509"] is not None)
    print("Certificate Loaded   :", result["certificate"] is not None)

    print()

    print("=" * 70)
    print("PASS")
    print("=" * 70)


if __name__ == "__main__":

    main()