import os

from config.config import PDCP_API_KEY
from core.logger import error
from modules.passive.helpers import execute_source


def run_chaos(domain: str) -> list[str]:

    if not PDCP_API_KEY:
        error("PDCP_API_KEY is not configured.")
        return []

    env = os.environ.copy()
    env["PDCP_API_KEY"] = PDCP_API_KEY

    command = [
        "chaos",
        "-d",
        domain,
        "-silent",
    ]

    return execute_source(
        name="Chaos",
        command=command,
        env=env,
    )