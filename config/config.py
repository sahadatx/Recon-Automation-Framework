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

SCREENSHOT_TIMEOUT = 15000

SCREENSHOT_WIDTH = 1440

SCREENSHOT_HEIGHT = 900

SCREENSHOT_FULL_PAGE = True

SCREENSHOT_WORKERS = 5

SCREENSHOT_OUTPUT = "output/screenshots"

HEADLESS_BROWSER = True



# ==========================================================
# URL Discovery
# ==========================================================

CRAWLER_DEPTH = 2

CRAWLER_TIMEOUT = 10

CRAWLER_MAX_URLS = 500

CRAWLER_DELAY = 0

CRAWLER_VERIFY_SSL = False

# ==========================================================
# URL Discovery
# ==========================================================

CRAWLER_DEPTH = 2

CRAWLER_MAX_URLS = 500

# ==========================================================
# URL Discovery
# ==========================================================

# Maximum crawl depth
CRAWLER_DEPTH = 2

# Maximum URLs to crawl per host
CRAWLER_MAX_URLS = 500

# HTTP timeout (seconds)
CRAWLER_TIMEOUT = 10

# Delay between requests (seconds)
CRAWLER_DELAY = 0

# Verify SSL certificates
CRAWLER_VERIFY_SSL = False

CRAWLER_WORKERS = 10

# ==========================================================
# Directory Fuzzing
# ==========================================================

FUZZ_THREADS = 40

FUZZ_TIMEOUT = 300

FUZZ_MATCH_CODES = (

    "200,204,301,302,307,401,403,405"

)

FUZZ_RECURSION = False

FUZZ_FOLLOW_REDIRECT = False

FUZZ_RATE = 0