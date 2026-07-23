"""
Subdomain Takeover Detection Constants

Centralized constants used by the
Subdomain Takeover Detection module.
"""

from __future__ import annotations

from pathlib import Path

from config.config import (
    HTTP_TIMEOUT,
)

# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path(
    "output/takeover",
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TXT_FILE = OUTPUT_DIR / "results.txt"

JSON_FILE = OUTPUT_DIR / "results.json"

CSV_FILE = OUTPUT_DIR / "results.csv"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

VULNERABLE_FILE = OUTPUT_DIR / "vulnerable.txt"

# ==========================================================
# Network Defaults
# ==========================================================

DEFAULT_HTTP_PORT = 80

DEFAULT_HTTPS_PORT = 443

DEFAULT_TIMEOUT = HTTP_TIMEOUT

MAX_REDIRECTS = 5

# ==========================================================
# Confidence Thresholds
# ==========================================================

HIGH_CONFIDENCE = 95

MEDIUM_CONFIDENCE = 70

LOW_CONFIDENCE = 40

UNKNOWN_CONFIDENCE = 0

# ==========================================================
# Detection Methods
# ==========================================================

METHOD_HTTP = "http"

METHOD_STATUS = "status"

METHOD_CNAME = "cname"

METHOD_DNS = "dns"

# ==========================================================
# Interesting Status Codes
# ==========================================================

STATUS_CODES = {

    400,

    403,

    404,

    410,

    421,

    451,

}

# ==========================================================
# Default HTTP Headers
# ==========================================================

DEFAULT_HEADERS = {

    "User-Agent": (

        "ReconAutomationFramework/1.0 "

        "(Subdomain Takeover Detection)"

    ),

    "Accept": "*/*",

    "Accept-Encoding": "gzip, deflate",

    "Connection": "close",

}

# ==========================================================
# Default Analysis Result
# ==========================================================

EMPTY_RESULT = {

    "target": "",

    "vulnerable": False,

    "provider": "",

    "confidence": UNKNOWN_CONFIDENCE,

    "methods": [],

    "status_code": 0,

    "fingerprint": "",

    "cname": "",

    "ip": "",

    "http_title": "",

    "recommendations": [],

    "error": None,

}

# ==========================================================
# Supported Takeover Providers
# ==========================================================

TAKEOVER_PROVIDERS = (

    "GitHub Pages",

    "Heroku",

    "ReadMe",

    "Surge",

    "Fastly",

    "Azure App Service",

    "Pantheon",

    "Zendesk",

    "Shopify",

    "Bitbucket",

    "Netlify",

    "Vercel",

    "AWS S3",

    "Ghost",

    "Cargo",

)

# ==========================================================
# HTTP Body Fingerprints
# ==========================================================

TAKEOVER_FINGERPRINTS = {

    "GitHub Pages": {

        "There isn't a GitHub Pages site here.",

    },

    "Heroku": {

        "No such app",

    },

    "ReadMe": {

        "Project doesnt exist",

        "Project doesn't exist",

    },

    "Surge": {

        "project not found",

    },

    "Fastly": {

        "Fastly error: unknown domain",

        "unknown domain",

    },

    "Azure App Service": {

        "404 Web Site not found",

        "The resource you are looking for has been removed",

    },

    "Pantheon": {

        "The gods are wise",

        "404 error unknown site",

    },

    "Zendesk": {

        "Help Center Closed",

    },

    "Shopify": {

        "Sorry, this shop is currently unavailable",

    },

    "Bitbucket": {

        "Repository not found",

    },

    "Netlify": {

        "Not Found - Request ID",

        "Page Not Found",

    },

    "Vercel": {

        "DEPLOYMENT_NOT_FOUND",

    },

    "AWS S3": {

        "NoSuchBucket",

        "The specified bucket does not exist",

    },

    "Ghost": {

        "The thing you were looking for is no longer here",

    },

    "Cargo": {

        "If you're moving your domain away from Cargo",

    },

}

# ==========================================================
# CNAME Fingerprints
# ==========================================================

CNAME_FINGERPRINTS = {

    "GitHub Pages": {

        ".github.io",

    },

    "Heroku": {

        ".herokudns.com",

        ".herokuapp.com",

    },

    "ReadMe": {

        ".readme.io",

    },

    "Surge": {

        ".surge.sh",

    },

    "Fastly": {

        ".fastly.net",

        ".fastlylb.net",

    },

    "Azure App Service": {

        ".azurewebsites.net",

    },

    "Pantheon": {

        ".pantheonsite.io",

    },

    "Zendesk": {

        ".zendesk.com",

    },

    "Shopify": {

        ".myshopify.com",

    },

    "Bitbucket": {

        ".bitbucket.io",

    },

    "Netlify": {

        ".netlify.app",

    },

    "Vercel": {

        ".vercel.app",

        ".vercel-dns.com",

    },

    "AWS S3": {

        ".s3.amazonaws.com",

        ".s3-website",

    },

    "Ghost": {

        ".ghost.io",

    },

    "Cargo": {

        ".cargo.site",

    },

}

# ==========================================================
# Recommendations
# ==========================================================

RECOMMENDATIONS = {

    True: [

        "Possible subdomain takeover detected.",

        "Verify the DNS configuration.",

        "Confirm the finding manually before reporting.",

        "Ensure the referenced service is still owned.",

    ],

    False: [

        "No takeover fingerprints were detected.",

    ],

}

# ==========================================================
# Export Fields
# ==========================================================

EXPORT_FIELDS = (

    "target",

    "vulnerable",

    "provider",

    "confidence",

    "methods",

    "status_code",

    "fingerprint",

    "cname",

    "ip",

    "http_title",

)

# ==========================================================
# Default Analysis
# ==========================================================

DEFAULT_ANALYSIS = {

    "target": "",

    "vulnerable": False,

    "provider": "",

    "confidence": UNKNOWN_CONFIDENCE,

    "methods": [],

    "status_code": 0,

    "fingerprint": "",

    "cname": "",

    "ip": "",

    "http_title": "",

    "recommendations": [],

    "error": None,

}

# ==========================================================
# Export
# ==========================================================

__all__ = [

    "OUTPUT_DIR",

    "TXT_FILE",

    "JSON_FILE",

    "CSV_FILE",

    "SUMMARY_FILE",

    "VULNERABLE_FILE",

    "DEFAULT_HTTP_PORT",

    "DEFAULT_HTTPS_PORT",

    "DEFAULT_TIMEOUT",

    "MAX_REDIRECTS",

    "HIGH_CONFIDENCE",

    "MEDIUM_CONFIDENCE",

    "LOW_CONFIDENCE",

    "UNKNOWN_CONFIDENCE",

    "METHOD_HTTP",

    "METHOD_STATUS",

    "METHOD_CNAME",

    "METHOD_DNS",

    "STATUS_CODES",

    "DEFAULT_HEADERS",

    "EMPTY_RESULT",

    "TAKEOVER_PROVIDERS",

    "TAKEOVER_FINGERPRINTS",

    "CNAME_FINGERPRINTS",

    "RECOMMENDATIONS",

    "EXPORT_FIELDS",

    "DEFAULT_ANALYSIS",

]

