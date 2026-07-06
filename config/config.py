"""
Global Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Recon Automation Framework"
VERSION = "2.0.0"
AUTHOR = "Sahadat Hossain"

DEFAULT_TIMEOUT = 60
MAX_WORKERS = 7

OUTPUT_DIR = "output"
REPORT_DIR = "reports"
LOG_DIR = "logs"

USER_AGENT = "ReconAutomationFramework/2.0"

PDCP_API_KEY = os.getenv("PDCP_API_KEY", "")
SECURITYTRAILS_API_KEY = os.getenv("SECURITYTRAILS_API_KEY", "")

# ==========================================================
# DNS Configuration
# ==========================================================

DNS_TIMEOUT = 5
DNS_LIFETIME = 8
DNS_RETRY = 1

DNS_SERVERS = [
    "1.1.1.1",
    "1.0.0.1",
]

# ==========================================================
# HTTP Configuration
# ==========================================================

HTTP_TIMEOUT = 8

HTTP_RETRIES = 1

VERIFY_SSL = False

USER_AGENT = (
    "ReconAutomationFramework/2.0"
)

# ==========================================================
# Logging Configuration
# ==========================================================

VERBOSE = False