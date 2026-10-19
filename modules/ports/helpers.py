import socket

from config.config import DEBUG, PORT_SCAN_TIMEOUT
from core.logger import debug


SERVICE_MAP = {

    80: "http",
    443: "https",
    8080: "http-alt",
    8081: "http-alt",
    8443: "https-alt",
    8000: "http-alt",
    8008: "http-alt",
    8088: "http-alt",

    22: "ssh",
    23: "telnet",
    3389: "rdp",
    5900: "vnc",

    25: "smtp",
    110: "pop3",
    143: "imap",
    465: "smtps",
    587: "submission",
    993: "imaps",
    995: "pop3s",

    53: "dns",

    445: "smb",

    1433: "mssql",
    1521: "oracle",
    3306: "mysql",
    5432: "postgresql",
    6379: "redis",
    27017: "mongodb",
    9200: "elasticsearch",
    9300: "elasticsearch",

    2375: "docker",
    2376: "docker-tls",
    6443: "kubernetes",

    8888: "jupyter",
    9090: "prometheus",
    9000: "sonarqube",
    10000: "webmin",
}


def create_socket():


    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM,
    )

    sock.settimeout(PORT_SCAN_TIMEOUT)

    return sock


def get_service_name(
    port: int,
) -> str:


    return SERVICE_MAP.get(
        port,
        "unknown",
    )


def scan_port(
    host: str,
    port: int,
):


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


def show_scan(
    host: str,
    port: int,
):


    if DEBUG:

        debug(f"Scanning {host}:{port}")


def get_timeout():


    return PORT_SCAN_TIMEOUT
