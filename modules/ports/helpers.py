"""
Port Scanner Helper Functions

Shared helper functions used by the
Port Scanner module.
"""

import socket

from config.config import (
    PORT_SCAN_TIMEOUT,
    DEBUG,
)

from core.logger import (
    debug,
)


# ==========================================================
# Common Services
# ==========================================================

SERVICE_MAP = {

    # Web
    80: "http",
    443: "https",
    8080: "http-alt",
    8081: "http-alt",
    8443: "https-alt",
    8000: "http-alt",
    8008: "http-alt",
    8088: "http-alt",

    # Remote Access
    22: "ssh",
    23: "telnet",
    3389: "rdp",
    5900: "vnc",

    # Mail
    25: "smtp",
    110: "pop3",
    143: "imap",
    465: "smtps",
    587: "submission",
    993: "imaps",
    995: "pop3s",

    # DNS
    53: "dns",

    # SMB
    445: "smb",

    # Databases
    1433: "mssql",
    1521: "oracle",
    3306: "mysql",
    5432: "postgresql",
    6379: "redis",
    27017: "mongodb",
    9200: "elasticsearch",
    9300: "elasticsearch",

    # Containers
    2375: "docker",
    2376: "docker-tls",
    6443: "kubernetes",

    # Misc
    8888: "jupyter",
    9090: "prometheus",
    9000: "sonarqube",
    10000: "webmin",

}


# ==========================================================
# Create Socket
# ==========================================================

def create_socket():
    """
    Create a configured TCP socket.
    """

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    sock.settimeout(
        PORT_SCAN_TIMEOUT
    )

    return sock


# ==========================================================
# Get Service Name
# ==========================================================

def get_service_name(
    port: int,
) -> str:
    """
    Return a friendly service name.
    """

    return SERVICE_MAP.get(
        port,
        "unknown",
    )


# ==========================================================
# Scan Port
# ==========================================================

def scan_port(
    host: str,
    port: int,
):
    """
    Scan one TCP port.

    Returns:
        dict | None
    """

    sock = create_socket()

    try:

        result = sock.connect_ex(
            (
                host,
                port,
            )
        )

        if result != 0:
            return None

        return {

            "port": port,

            "service": get_service_name(
                port,
            ),

            "state": "open",

            # Future:
            "banner": None,

        }

    except (
        socket.timeout,
        socket.gaierror,
        ConnectionRefusedError,
        OSError,
    ):

        return None

    finally:

        sock.close()


# ==========================================================
# Show Scan
# ==========================================================

def show_scan(
    host: str,
    port: int,
):
    """
    Display scan information.
    """

    if DEBUG:

        debug(
            f"Scanning {host}:{port}"
        )


# ==========================================================
# Get Timeout
# ==========================================================

def get_timeout():
    """
    Return configured timeout.
    """

    return PORT_SCAN_TIMEOUT