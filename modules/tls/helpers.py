"""
TLS Helpers

Reusable helper functions for
TLS Analysis.
"""

from __future__ import annotations

import socket
import ssl

from copy import deepcopy
from datetime import datetime
from typing import Any

from config.config import HTTP_TIMEOUT


# ==========================================================
# Default Result
# ==========================================================

EMPTY_CERTIFICATE = {

    "host": "",

    "port": 443,

    "tls_version": "",

    "cipher": "",

    "certificate": None,

    "certificate_der": None,

    "error": None,

}


# ==========================================================
# SSL Context
# ==========================================================

def create_ssl_context():
    """
    Create SSL context.

    Returns:
        ssl.SSLContext
    """

    context = ssl.create_default_context()

    context.check_hostname = False

    context.verify_mode = ssl.CERT_REQUIRED

    return context


# ==========================================================
# TCP Connection
# ==========================================================

def create_socket(
    host: str,
    port: int = 443,
    timeout: int = HTTP_TIMEOUT,
):
    """
    Create TCP socket.

    Returns:
        socket.socket
    """

    return socket.create_connection(

        (host, port),

        timeout=timeout,

    )


# ==========================================================
# TLS Connection
# ==========================================================

def connect_tls(
    host: str,
    port: int = 443,
):
    """
    Create TLS connection.

    Returns:
        ssl.SSLSocket
    """

    context = create_ssl_context()

    raw_socket = create_socket(

        host,

        port,

    )

    tls_socket = context.wrap_socket(

        raw_socket,

        server_hostname=host,

    )

    return tls_socket


# ==========================================================
# Download Certificate
# ==========================================================

def get_certificate(
    host: str,
    port: int = 443,
):
    """
    Download peer certificate.

    Returns:
        dict
    """

    result = deepcopy(

        EMPTY_CERTIFICATE

    )

    result["host"] = host

    result["port"] = port

    tls_socket = None

    try:

        tls_socket = connect_tls(

            host,

            port,

        )

        result["certificate"] = (

            tls_socket.getpeercert(

                binary_form=False,

            )

        )

        result["certificate_der"] = (

            tls_socket.getpeercert(

                binary_form=True,

            )

        )

        result["tls_version"] = (

            tls_socket.version()

        )

        cipher = tls_socket.cipher()

        if cipher:

            result["cipher"] = cipher[0]

    except Exception as exc:

        result["error"] = str(exc)

    finally:

        if tls_socket:

            tls_socket.close()

    return result


# ==========================================================
# Parse X509 Name
# ==========================================================

def parse_name(
    name,
):
    """
    Convert X509 name tuple
    into dictionary.

    Returns:
        dict
    """

    result = {}

    if not name:

        return result

    for item in name:

        for key, value in item:

            result[key] = value

    return result


# ==========================================================
# Subject
# ==========================================================

def get_subject(
    certificate,
):
    """
    Extract certificate subject.

    Returns:
        dict
    """

    if not certificate:

        return {}

    return parse_name(

        certificate.get(

            "subject",

            (),

        )

    )


# ==========================================================
# Issuer
# ==========================================================

def get_issuer(
    certificate,
):
    """
    Extract certificate issuer.

    Returns:
        dict
    """

    if not certificate:

        return {}

    return parse_name(

        certificate.get(

            "issuer",

            (),

        )

    )


# ==========================================================
# Subject Alternative Names
# ==========================================================

def get_san(
    certificate,
):
    """
    Extract Subject
    Alternative Names.

    Returns:
        list
    """

    if not certificate:

        return []

    san = []

    for key, value in certificate.get(

        "subjectAltName",

        (),

    ):

        if key == "DNS":

            san.append(

                value

            )

    return sorted(

        set(san)

    )


# ==========================================================
# Serial Number
# ==========================================================

def get_serial_number(
    certificate,
):
    """
    Extract serial number.

    Returns:
        str
    """

    if not certificate:

        return ""

    return certificate.get(

        "serialNumber",

        "",

    )


# ==========================================================
# Not Before
# ==========================================================

def get_not_before(
    certificate,
):
    """
    Extract notBefore.

    Returns:
        str
    """

    if not certificate:

        return ""

    return certificate.get(

        "notBefore",

        "",

    )


# ==========================================================
# Not After
# ==========================================================

def get_not_after(
    certificate,
):
    """
    Extract notAfter.

    Returns:
        str
    """

    if not certificate:

        return ""

    return certificate.get(

        "notAfter",

        "",

    )


# ==========================================================
# Parse Datetime
# ==========================================================

def parse_datetime(
    value: str,
):
    """
    Convert certificate datetime
    string into datetime object.

    Returns:
        datetime | None
    """

    if not value:

        return None

    try:

        return datetime.strptime(

            value,

            "%b %d %H:%M:%S %Y %Z",

        )

    except Exception:

        return None


# ==========================================================
# Days Remaining
# ==========================================================

def days_remaining(
    certificate,
):
    """
    Calculate certificate
    remaining days.

    Returns:
        int | None
    """

    expires = parse_datetime(

        get_not_after(

            certificate,

        )

    )

    if expires is None:

        return None

    return (

        expires - datetime.utcnow()

    ).days


# ==========================================================
# Expired
# ==========================================================

def is_expired(
    certificate,
):
    """
    Check whether certificate
    is expired.

    Returns:
        bool
    """

    remaining = days_remaining(

        certificate,

    )

    if remaining is None:

        return False

    return remaining < 0


# ==========================================================
# Self Signed
# ==========================================================

def is_self_signed(
    certificate,
):
    """
    Check self-signed certificate.

    Returns:
        bool
    """

    return (

        get_subject(

            certificate,

        )

        ==

        get_issuer(

            certificate,

        )

    )


# ==========================================================
# Wildcard
# ==========================================================

def is_wildcard(
    certificate,
):
    """
    Check wildcard certificate.

    Returns:
        bool
    """

    subject = get_subject(

        certificate,

    )

    common_name = subject.get(

        "commonName",

        "",

    )

    return common_name.startswith(

        "*.",

    )


# ==========================================================
# Hostname Match
# ==========================================================

def hostname_match(
    host: str,
    certificate,
):
    """
    Verify hostname.

    Returns:
        bool
    """

    if not certificate:

        return False

    san = get_san(

        certificate,

    )

    if host in san:

        return True

    subject = get_subject(

        certificate,

    )

    common_name = subject.get(

        "commonName",

        "",

    )

    if common_name.startswith("*."):

        domain = common_name[2:]

        return (

            host == domain

            or

            host.endswith(

                "." + domain

            )

        )

    return host == common_name


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "EMPTY_CERTIFICATE",

    "create_ssl_context",

    "create_socket",

    "connect_tls",

    "get_certificate",

    "parse_name",

    "get_subject",

    "get_issuer",

    "get_san",

    "get_serial_number",

    "get_not_before",

    "get_not_after",

    "parse_datetime",

    "days_remaining",

    "is_expired",

    "is_self_signed",

    "is_wildcard",

    "hostname_match",

]