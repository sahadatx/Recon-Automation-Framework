from __future__ import annotations

import socket
import ssl
from copy import deepcopy

from config.config import HTTP_TIMEOUT


EMPTY_PROTOCOL = {
    "host": "",
    "port": 443,
    "tls13": False,
    "tls12": False,
    "tls11": False,
    "tls10": False,
    "ssl3": False,
    "ssl2": False,
    "highest_protocol": "",
    "security": "",
    "error": None,
}


def create_protocol_context(
    version: ssl.TLSVersion,
):


    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_CLIENT,
    )

    context.check_hostname = False

    context.verify_mode = ssl.CERT_NONE

    context.minimum_version = version

    context.maximum_version = version

    return context


def test_protocol(
    host: str,
    version: ssl.TLSVersion,
    port: int = 443,
):


    sock = None

    tls = None

    try:

        context = create_protocol_context(
            version,
        )

        sock = socket.create_connection(
            (
                host,
                port,
            ),
            timeout=HTTP_TIMEOUT,
        )

        tls = context.wrap_socket(
            sock,
            server_hostname=host,
        )

        tls.do_handshake()

        expected_versions = {
            ssl.TLSVersion.TLSv1: "TLSv1",
            ssl.TLSVersion.TLSv1_1: "TLSv1.1",
            ssl.TLSVersion.TLSv1_2: "TLSv1.2",
            ssl.TLSVersion.TLSv1_3: "TLSv1.3",
        }

        negotiated = tls.version()

        expected = expected_versions.get(
            version,
        )

        return negotiated == expected

    except Exception:

        return False

    finally:

        if tls:

            tls.close()

        elif sock:

            sock.close()


def supports_tls13(
    host: str,
    port: int = 443,
):


    return test_protocol(
        host,
        ssl.TLSVersion.TLSv1_3,
        port,
    )


def supports_tls12(
    host: str,
    port: int = 443,
):


    return test_protocol(
        host,
        ssl.TLSVersion.TLSv1_2,
        port,
    )


def supports_tls11(
    host: str,
    port: int = 443,
):


    return test_protocol(
        host,
        ssl.TLSVersion.TLSv1_1,
        port,
    )


def supports_tls10(
    host: str,
    port: int = 443,
):


    return test_protocol(
        host,
        ssl.TLSVersion.TLSv1,
        port,
    )


def supports_ssl3(
    host: str,
    port: int = 443,
):


    try:

        version = ssl.TLSVersion.SSLv3

    except AttributeError:

        return False

    return test_protocol(
        host,
        version,
        port,
    )


def supports_ssl2(
    host: str,
    port: int = 443,
):


    return False


def highest_protocol(
    result: dict,
):


    if result["tls13"]:

        return "TLSv1.3"

    if result["tls12"]:

        return "TLSv1.2"

    if result["tls11"]:

        return "TLSv1.1"

    if result["tls10"]:

        return "TLSv1"

    if result["ssl3"]:

        return "SSLv3"

    if result["ssl2"]:

        return "SSLv2"

    return ""


def protocol_security(
    protocol: str,
):


    if protocol == "TLSv1.3":

        return "Excellent"

    if protocol == "TLSv1.2":

        return "Good"

    if protocol == "TLSv1.1":

        return "Weak"

    if protocol == "TLSv1":

        return "Weak"

    if protocol == "SSLv3":

        return "Insecure"

    if protocol == "SSLv2":

        return "Critical"

    return "Unknown"


def collect_protocols(
    host: str,
    port: int = 443,
):


    result = deepcopy(
        EMPTY_PROTOCOL,
    )

    result["host"] = host

    result["port"] = port

    try:

        result["tls13"] = supports_tls13(
            host,
            port,
        )

        result["tls12"] = supports_tls12(
            host,
            port,
        )

        result["tls11"] = supports_tls11(
            host,
            port,
        )

        result["tls10"] = supports_tls10(
            host,
            port,
        )

        result["ssl3"] = supports_ssl3(
            host,
            port,
        )

        result["ssl2"] = supports_ssl2(
            host,
            port,
        )

        result["highest_protocol"] = highest_protocol(
            result,
        )

        result["security"] = protocol_security(
            result["highest_protocol"],
        )

    except Exception as exc:

        result["error"] = str(
            exc,
        )

    return result


def protocol_summary(
    protocol_data: dict,
):


    if not protocol_data:

        return {}

    return {
        "highest_protocol": protocol_data.get(
            "highest_protocol",
            "",
        ),
        "security": protocol_data.get(
            "security",
            "",
        ),
        "supported_protocols": [
            version
            for version, enabled in (
                ("TLSv1.3", protocol_data["tls13"]),
                ("TLSv1.2", protocol_data["tls12"]),
                ("TLSv1.1", protocol_data["tls11"]),
                ("TLSv1", protocol_data["tls10"]),
                ("SSLv3", protocol_data["ssl3"]),
                ("SSLv2", protocol_data["ssl2"]),
            )
            if enabled
        ],
    }


__all__ = [
    "EMPTY_PROTOCOL",
    "create_protocol_context",
    "test_protocol",
    "supports_tls13",
    "supports_tls12",
    "supports_tls11",
    "supports_tls10",
    "supports_ssl3",
    "supports_ssl2",
    "highest_protocol",
    "protocol_security",
    "collect_protocols",
    "protocol_summary",
]
