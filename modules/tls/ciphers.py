from __future__ import annotations

from copy import deepcopy

from .helpers import connect_tls


EMPTY_CIPHER = {
    "host": "",
    "port": 443,
    "name": "",
    "protocol": "",
    "bits": 0,
    "description": "",
    "key_exchange": "Unknown",
    "authentication": "Unknown",
    "encryption": "Unknown",
    "hash": "Unknown",
    "forward_secrecy": False,
    "aead": False,
    "weak": False,
    "strength": "Unknown",
    "error": None,
}


WEAK_KEYWORDS = (
    "RC4",
    "DES",
    "3DES",
    "NULL",
    "EXPORT",
    "MD5",
)

FORWARD_SECRECY_KEYWORDS = (
    "ECDHE",
    "DHE",
)

AEAD_KEYWORDS = (
    "GCM",
    "CHACHA20",
    "POLY1305",
    "CCM",
)


TLS_VERSION_MAP = {
    "TLSv1": "TLS 1.0",
    "TLSv1.1": "TLS 1.1",
    "TLSv1.2": "TLS 1.2",
    "TLSv1.3": "TLS 1.3",
}


def contains_keyword(
    text: str,
    keywords,
):


    if not text:

        return False

    upper = text.upper()

    return any(keyword.upper() in upper for keyword in keywords)


def split_cipher(
    cipher_name: str,
):


    if "_WITH_" not in cipher_name:

        return (
            "",
            "",
            "",
        )

    left, right = cipher_name.split(
        "_WITH_",
        1,
    )

    left = left.replace(
        "TLS_",
        "",
    ).replace(
        "SSL_",
        "",
    )

    parts = right.split(
        "_",
    )

    if len(parts) == 1:

        encryption = parts[0]

        digest = ""

    else:

        encryption = "_".join(
            parts[:-1],
        )

        digest = parts[-1]

    return (
        left,
        encryption,
        digest,
    )


def detect_cipher(
    host: str,
    port: int = 443,
):


    tls = None

    try:

        tls = connect_tls(
            host,
            port,
        )

        return tls.cipher()

    finally:

        if tls:

            tls.close()


def cipher_name(
    cipher,
):


    if not cipher:

        return ""

    return cipher[0]


def cipher_protocol(
    cipher,
):


    if not cipher:

        return ""

    protocol = cipher[1]

    return TLS_VERSION_MAP.get(
        protocol,
        protocol,
    )


def cipher_bits(
    cipher,
):


    if not cipher:

        return 0

    try:

        return int(
            cipher[2],
        )

    except Exception:

        return 0


def key_exchange(
    cipher_name: str,
):


    exchange, _, _ = split_cipher(
        cipher_name,
    )

    if not exchange:

        return "Unknown"

    return exchange


def authentication(
    cipher_name: str,
):


    exchange = key_exchange(
        cipher_name,
    )

    upper = exchange.upper()

    if "ECDSA" in upper:

        return "ECDSA"

    if "RSA" in upper:

        return "RSA"

    if "PSK" in upper:

        return "PSK"

    return "Unknown"


def encryption_algorithm(
    cipher_name: str,
):


    _, encryption, _ = split_cipher(
        cipher_name,
    )

    if not encryption:

        return "Unknown"

    return encryption


def hash_algorithm(
    cipher_name: str,
):


    _, _, digest = split_cipher(
        cipher_name,
    )

    if not digest:

        return "Unknown"

    return digest


def forward_secrecy(
    cipher_name: str,
    protocol: str,
):


    if protocol in (
        "TLS 1.3",
        "TLSv1.3",
    ):

        return True

    return contains_keyword(
        cipher_name,
        FORWARD_SECRECY_KEYWORDS,
    )


def is_aead_cipher(
    cipher_name: str,
):


    return contains_keyword(
        cipher_name,
        AEAD_KEYWORDS,
    )


def is_weak_cipher(
    cipher_name: str,
):


    return contains_keyword(
        cipher_name,
        WEAK_KEYWORDS,
    )


def cipher_strength(
    cipher_name: str,
    bits: int,
):


    if is_weak_cipher(
        cipher_name,
    ):

        return "Insecure"

    if bits >= 256:

        return "Excellent"

    if bits >= 128:

        return "Good"

    if bits >= 112:

        return "Fair"

    if bits > 0:

        return "Weak"

    return "Unknown"


def collect_cipher(
    host: str,
    port: int = 443,
):


    result = deepcopy(
        EMPTY_CIPHER,
    )

    result["host"] = host

    result["port"] = port

    try:

        cipher = detect_cipher(
            host,
            port,
        )

        if not cipher:

            result["error"] = "No cipher negotiated."

            return result

        name = cipher_name(
            cipher,
        )

        bits = cipher_bits(
            cipher,
        )

        result["name"] = name

        result["protocol"] = cipher_protocol(
            cipher,
        )

        result["bits"] = bits

        result["description"] = f"{name} ({bits}-bit)"

        result["key_exchange"] = key_exchange(
            name,
        )

        result["authentication"] = authentication(
            name,
        )

        result["encryption"] = encryption_algorithm(
            name,
        )

        result["hash"] = hash_algorithm(
            name,
        )

        result["forward_secrecy"] = forward_secrecy(
            name,
            result["protocol"],
        )

        result["aead"] = is_aead_cipher(
            name,
        )

        result["weak"] = is_weak_cipher(
            name,
        )

        result["strength"] = cipher_strength(
            name,
            bits,
        )

    except Exception as exc:

        result["error"] = str(
            exc,
        )

    return result


def cipher_summary(
    cipher_data: dict,
):


    if not cipher_data:

        return {}

    return {
        "cipher": cipher_data.get(
            "name",
            "",
        ),
        "protocol": cipher_data.get(
            "protocol",
            "",
        ),
        "bits": cipher_data.get(
            "bits",
            0,
        ),
        "strength": cipher_data.get(
            "strength",
            "",
        ),
        "forward_secrecy": cipher_data.get(
            "forward_secrecy",
            False,
        ),
        "aead": cipher_data.get(
            "aead",
            False,
        ),
        "weak": cipher_data.get(
            "weak",
            False,
        ),
    }


__all__ = [
    "EMPTY_CIPHER",
    "detect_cipher",
    "cipher_name",
    "cipher_protocol",
    "cipher_bits",
    "key_exchange",
    "authentication",
    "encryption_algorithm",
    "hash_algorithm",
    "forward_secrecy",
    "is_aead_cipher",
    "is_weak_cipher",
    "cipher_strength",
    "collect_cipher",
    "cipher_summary",
]
