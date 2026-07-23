"""
TLS Certificate

Certificate collection and
analysis functions.
"""

from __future__ import annotations


from copy import deepcopy

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import (
    dsa,
    ec,
    ed25519,
    ed448,
    rsa,
)

from modules.tls.helpers import (
    get_certificate,
    get_subject,
    get_issuer,
    get_san,
    get_serial_number,
    get_not_before,
    get_not_after,
)


# ==========================================================
# Default Result
# ==========================================================

EMPTY_CERTIFICATE = {

    "host": "",

    "port": 443,

    "tls_version": "",

    "cipher": "",

    "subject": {},

    "issuer": {},

    "san": [],

    "serial_number": "",

    "signature_algorithm": "",

    "certificate_version": "",

    "public_key_type": "",

    "public_key_size": 0,

    "sha1": "",

    "sha256": "",

    "not_before": "",

    "not_after": "",

    "certificate": None,

    "x509": None,

    "error": None,

}


# ==========================================================
# Load X509 Certificate
# ==========================================================

def load_x509_certificate(
    host: str,
    port: int = 443,
):
    """
    Download and load
    X509 certificate.

    Returns:
        tuple
    """

    tls = get_certificate(

        host,

        port,

    )

    if tls["error"]:

        return (

            tls,

            None,

        )

    try:

        der = tls["certificate_der"]

        pem = x509.load_der_x509_certificate(

            der,

        )

        return (

            tls,

            pem,

        )

    except Exception as exc:

        tls["error"] = str(exc)

        return (

            tls,

            None,

        )


# ==========================================================
# SHA1 Fingerprint
# ==========================================================

def get_sha1(
    certificate: x509.Certificate,
):
    """
    SHA1 fingerprint.

    Returns:
        str
    """

    if certificate is None:

        return ""

    return (

        certificate.fingerprint(

            hashes.SHA1(),

        )

        .hex()

        .upper()

    )


# ==========================================================
# SHA256 Fingerprint
# ==========================================================

def get_sha256(
    certificate: x509.Certificate,
):
    """
    SHA256 fingerprint.

    Returns:
        str
    """

    if certificate is None:

        return ""

    return (

        certificate.fingerprint(

            hashes.SHA256(),

        )

        .hex()

        .upper()

    )

# ==========================================================
# Certificate Version
# ==========================================================

def get_certificate_version(
    certificate: x509.Certificate,
):
    """
    Get certificate version.

    Returns:
        str
    """

    if certificate is None:

        return ""

    version = certificate.version

    if version == x509.Version.v1:

        return "v1"

    if version == x509.Version.v3:

        return "v3"

    return str(version)


# ==========================================================
# Signature Algorithm
# ==========================================================

def get_signature_algorithm(
    certificate: x509.Certificate,
):
    """
    Get signature algorithm.

    Returns:
        str
    """

    if certificate is None:

        return ""

    try:

        return (

            certificate.signature_hash_algorithm.name

        )

    except Exception:

        return ""


# ==========================================================
# Public Key
# ==========================================================

def get_public_key(
    certificate: x509.Certificate,
):
    """
    Return public key object.

    Returns:
        object | None
    """

    if certificate is None:

        return None

    try:

        return certificate.public_key()

    except Exception:

        return None


# ==========================================================
# Public Key Type
# ==========================================================

def get_public_key_type(
    certificate: x509.Certificate,
):
    """
    Detect public key type.

    Returns:
        str
    """

    key = get_public_key(

        certificate,

    )

    if key is None:

        return ""

    if isinstance(

        key,

        rsa.RSAPublicKey,

    ):

        return "RSA"

    if isinstance(

        key,

        ec.EllipticCurvePublicKey,

    ):

        return "EC"

    if isinstance(

        key,

        dsa.DSAPublicKey,

    ):

        return "DSA"

    if isinstance(

        key,

        ed25519.Ed25519PublicKey,

    ):

        return "Ed25519"

    if isinstance(

        key,

        ed448.Ed448PublicKey,

    ):

        return "Ed448"

    return type(

        key,

    ).__name__


# ==========================================================
# Public Key Size
# ==========================================================

def get_public_key_size(
    certificate: x509.Certificate,
):
    """
    Get public key size.

    Returns:
        int
    """

    key = get_public_key(

        certificate,

    )

    if key is None:

        return 0

    return getattr(

        key,

        "key_size",

        0,

    )


# ==========================================================
# Certificate Summary
# ==========================================================

def certificate_summary(
    certificate: x509.Certificate,
):
    """
    Generate certificate summary.

    Returns:
        dict
    """

    if certificate is None:

        return {}

    return {

        "certificate_version":

            get_certificate_version(

                certificate,

            ),

        "signature_algorithm":

            get_signature_algorithm(

                certificate,

            ),

        "public_key_type":

            get_public_key_type(

                certificate,

            ),

        "public_key_size":

            get_public_key_size(

                certificate,

            ),

        "sha1":

            get_sha1(

                certificate,

            ),

        "sha256":

            get_sha256(

                certificate,

            ),

    }


# ==========================================================
# Collect Certificate
# ==========================================================

def collect_certificate(
    host: str,
    port: int = 443,
):
    """
    Collect TLS certificate
    information.

    Returns:
        dict
    """

    result = deepcopy(

        EMPTY_CERTIFICATE,

    )

    tls, certificate = load_x509_certificate(

        host,

        port,

    )

    result["host"] = host

    result["port"] = port

    result["tls_version"] = tls.get(

        "tls_version",

        "",

    )

    result["cipher"] = tls.get(

        "cipher",

        "",

    )

    result["error"] = tls.get(

        "error",

    )

    if certificate is None:

        return result

    cert = tls.get(

        "certificate",

    )

    result["subject"] = get_subject(

        cert,

    )

    result["issuer"] = get_issuer(

        cert,

    )

    result["san"] = get_san(

        cert,

    )

    result["serial_number"] = get_serial_number(

        cert,

    )

    result["not_before"] = get_not_before(

        cert,

    )

    result["not_after"] = get_not_after(

        cert,

    )

    summary = certificate_summary(

        certificate,

    )

    result.update(

        summary,

    )

    result["certificate"] = cert

    result["x509"] = certificate

    return result


# ==========================================================
# Export
# ==========================================================

__all__ = [

    "EMPTY_CERTIFICATE",

    "load_x509_certificate",

    "get_sha1",

    "get_sha256",

    "get_certificate_version",

    "get_signature_algorithm",

    "get_public_key",

    "get_public_key_type",

    "get_public_key_size",

    "certificate_summary",

    "collect_certificate",

]

