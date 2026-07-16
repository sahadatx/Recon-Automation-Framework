"""
Global Configuration

Central configuration for the
Recon Automation Framework.
"""

import os

from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# Load Environment
# ==========================================================

load_dotenv()


# ==========================================================
# Application
# ==========================================================

APP_NAME = (

    "Recon Automation Framework"

)

VERSION = (

    "1.0.0"

)

AUTHOR = (

    "Sahadat Hossain"

)


# ==========================================================
# Framework
# ==========================================================

DEFAULT_TIMEOUT = 60

MAX_WORKERS = 7

USER_AGENT = (

    "ReconAutomationFramework/1.0.0"

)

DEFAULT_ENCODING = (

    "utf-8"

)

DEFAULT_SCHEME = (

    "https"

)


# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = (

    Path.cwd()

)

OUTPUT_DIR = (

    PROJECT_ROOT

    / "output"

)

LOG_DIR = (

    PROJECT_ROOT

    / "logs"

)

TEMP_DIR = (

    PROJECT_ROOT

    / "temp"

)


PASSIVE_OUTPUT_DIR = (

    OUTPUT_DIR

    / "passive"

)

DNS_OUTPUT_DIR = (

    OUTPUT_DIR

    / "dns"

)

HTTP_OUTPUT_DIR = (

    OUTPUT_DIR

    / "http"

)

PORT_OUTPUT_DIR = (

    OUTPUT_DIR

    / "ports"

)

TECHNOLOGY_OUTPUT_DIR = (

    OUTPUT_DIR

    / "technology"

)

CRAWLER_OUTPUT_DIR = (

    OUTPUT_DIR

    / "crawler"

)

JAVASCRIPT_OUTPUT_DIR = (

    OUTPUT_DIR

    / "javascript"

    / "raw"

)

FUZZ_OUTPUT_DIR = (

    OUTPUT_DIR

    / "fuzzing"

)

SCREENSHOT_OUTPUT_DIR = (

    OUTPUT_DIR

    / "screenshots"

)

NUCLEI_OUTPUT_DIR = (

    OUTPUT_DIR

    / "nuclei"

)

VHOST_OUTPUT_DIR = (

    OUTPUT_DIR

    / "vhost"

)


# ==========================================================
# Shared Wordlists
# ==========================================================

WORDLISTS_DIR = (

    PROJECT_ROOT

    / "wordlists"

)

DIRECTORY_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "directories"

)

VHOST_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "vhosts"

)

SUBDOMAIN_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "subdomains"

)

PARAMETER_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "parameters"

)

FILES_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "files"

)

CUSTOM_WORDLIST_DIR = (

    WORDLISTS_DIR

    / "custom"

)


# ==========================================================
# Default Wordlists
# ==========================================================

DEFAULT_DIRECTORY_WORDLIST = (

    DIRECTORY_WORDLIST_DIR

    / "common.txt"

)

DEFAULT_VHOST_WORDLIST = (

    VHOST_WORDLIST_DIR

    / "common.txt"

)

DEFAULT_SUBDOMAIN_WORDLIST = (

    SUBDOMAIN_WORDLIST_DIR

    / "common.txt"

)

DEFAULT_PARAMETER_WORDLIST = (

    PARAMETER_WORDLIST_DIR

    / "common.txt"

)


# ==========================================================
# API Keys
# ==========================================================

PDCP_API_KEY = (

    os.getenv(

        "PDCP_API_KEY",

        "",

    )

)

SECURITYTRAILS_API_KEY = (

    os.getenv(

        "SECURITYTRAILS_API_KEY",

        "",

    )

)

CHAOS_API_KEY = (

    os.getenv(

        "CHAOS_API_KEY",

        "",

    )

)

SHODAN_API_KEY = (

    os.getenv(

        "SHODAN_API_KEY",

        "",

    )

)


# ==========================================================
# DNS Configuration
# ==========================================================

DNS_TIMEOUT = 5

DNS_LIFETIME = 8

DNS_RETRIES = 1

DNS_SERVERS = [

    "1.1.1.1",

    "1.0.0.1",

    "8.8.8.8",

    "8.8.4.4",

]


# ==========================================================
# HTTP Configuration
# ==========================================================

HTTP_TIMEOUT = 8

HTTP_RETRIES = 1

HTTP_THREADS = 50

HTTP_VERIFY_SSL = False

HTTP_FOLLOW_REDIRECTS = True

HTTP_USER_AGENT = (

    USER_AGENT

)


# ==========================================================
# Port Scanner Configuration
# ==========================================================

PORT_SCAN_TIMEOUT = 1

PORT_SCAN_RETRIES = 1

PORT_HOST_WORKERS = 30

PORT_SCAN_WORKERS = 100

ENABLE_BANNER_GRAB = False

DEFAULT_PORTS = (

    "common"

)


# ==========================================================
# URL Discovery (Crawler)
# ==========================================================

CRAWLER_DEPTH = 2

CRAWLER_MAX_URLS = 500

CRAWLER_TIMEOUT = 10

CRAWLER_DELAY = 0

CRAWLER_THREADS = 10

CRAWLER_RETRIES = 3

CRAWLER_FOLLOW_REDIRECTS = True


# ==========================================================
# Screenshot Configuration
# ==========================================================

SCREENSHOT_WIDTH = 1440

SCREENSHOT_HEIGHT = 900

SCREENSHOT_TIMEOUT = 15000

SCREENSHOT_WORKERS = 5

SCREENSHOT_FULL_PAGE = True

SCREENSHOT_HEADLESS = True

SCREENSHOT_DARK_MODE = False

SCREENSHOT_FORMAT = (

    "png"

)

SCREENSHOT_QUALITY = 100



# ==========================================================
# Directory Fuzzing
# ==========================================================

FUZZ_THREADS = 40

FUZZ_TIMEOUT = 300

FUZZ_RATE_LIMIT = 100

FUZZ_RETRIES = 1

FUZZ_RECURSION = False

FUZZ_FOLLOW_REDIRECTS = False

FUZZ_AUTO_CALIBRATION = True

FUZZ_DEFAULT_WORDLIST = (

    DEFAULT_DIRECTORY_WORDLIST

)

FUZZ_MATCH_CODES = (

    "200,204,301,302,307,401,403,405"

)

FUZZ_FILTER_CODES = (

    "400,404"

)

FUZZ_MATCH_SIZE = ""

FUZZ_FILTER_SIZE = "0"


# ==========================================================
# Nuclei Configuration
# ==========================================================

NUCLEI_THREADS = 25

NUCLEI_TIMEOUT = 600

NUCLEI_RATE_LIMIT = 150

NUCLEI_RETRIES = 2

NUCLEI_PROFILE = (

    "default"

)

NUCLEI_SEVERITY = (

    "critical,high,medium,low,info"

)

NUCLEI_FOLLOW_REDIRECTS = False


# ==========================================================
# Virtual Host Discovery
# ==========================================================

VHOST_THREADS = 40

VHOST_TIMEOUT = 300

VHOST_RATE_LIMIT = 150

VHOST_AUTO_CALIBRATION = True

VHOST_RETRIES = 1

VHOST_HEADER = (

    "Host"

)

VHOST_DEFAULT_WORDLIST = (

    DEFAULT_VHOST_WORDLIST

)

VHOST_RECURSION = False

VHOST_FOLLOW_REDIRECTS = False

VHOST_MATCH_CODES = (

    "200,204,301,302,307,401,403"

)

VHOST_FILTER_CODES = (

    "400,404"

)

VHOST_MATCH_SIZE = ""

VHOST_FILTER_SIZE = "0"


# ==========================================================
# Logging Configuration
# ==========================================================

VERBOSE = False

LOG_LEVEL = (

    "INFO"

)

LOG_TO_FILE = True

LOG_FILE = (

    LOG_DIR

    / "framework.log"

)


# ==========================================================
# Debug Configuration
# ==========================================================

DEBUG = False

SAVE_RAW_OUTPUT = False

KEEP_TEMP_FILES = False

SHOW_TOOL_COMMANDS = False


# ==========================================================
# Export Configuration
# ==========================================================

DEFAULT_OUTPUT_FORMATS = [

    "txt",

    "json",

    "csv",

    "markdown",

]