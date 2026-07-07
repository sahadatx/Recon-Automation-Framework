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

# ==========================================================
# Port Scanner
# ==========================================================

PORT_SCAN_TIMEOUT = 1

PORT_SCAN_RETRY = 1

# Parallel Hosts
PORT_HOST_WORKERS = 30

# Parallel Ports
PORT_SCAN_WORKERS = 100

# Banner Grabbing
ENABLE_BANNER_GRAB = False

# Default TCP ports to scan
DEFAULT_PORTS = "common"

# ==========================================================
# Debug
# ==========================================================

DEBUG = False

# ==========================================================
# Screenshot
# ==========================================================

SCREENSHOT_TIMEOUT = 60000

SCREENSHOT_WIDTH = 1440

SCREENSHOT_HEIGHT = 900

SCREENSHOT_FULL_PAGE = True

SCREENSHOT_WORKERS = 5

SCREENSHOT_OUTPUT = "output/screenshots"

HEADLESS_BROWSER = True

