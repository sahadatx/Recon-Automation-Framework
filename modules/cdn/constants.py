"""
CDN Detection Constants

Centralized constants used by the CDN Detection module.
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
    "output/cdn"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

TXT_FILE = OUTPUT_DIR / "results.txt"

JSON_FILE = OUTPUT_DIR / "results.json"

CSV_FILE = OUTPUT_DIR / "results.csv"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

DETECTED_FILE = OUTPUT_DIR / "detected.txt"

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

HIGH_CONFIDENCE = 90

MEDIUM_CONFIDENCE = 70

LOW_CONFIDENCE = 50

UNKNOWN_CONFIDENCE = 0

# ==========================================================
# Detection Methods
# ==========================================================

METHOD_HEADER = "header"

METHOD_CNAME = "cname"

METHOD_SERVER = "server"

METHOD_CACHE = "cache"

METHOD_DNS = "dns"

METHOD_IP = "ip"

METHOD_TLS = "tls"

# ==========================================================
# Default HTTP Headers
# ==========================================================

DEFAULT_HEADERS = {

    "User-Agent": (

        "ReconAutomationFramework/1.0 "

        "(CDN Detection)"

    ),

    "Accept": "*/*",

    "Accept-Encoding": "gzip, deflate",

    "Connection": "close",

}

# ==========================================================
# Common CDN Headers
# ==========================================================

COMMON_CDN_HEADERS = (

    "server",

    "via",

    "x-cache",

    "x-cache-hits",

    "cf-cache-status",

    "cf-ray",

    "cf-request-id",

    "cf-worker",

    "cdn-loop",

    "x-served-by",

    "x-fastly-request-id",

    "x-amz-cf-id",

    "x-amz-cf-pop",

    "x-azure-ref",

    "x-msedge-ref",

    "x-cdn",

    "x-cdn-cache",

    "x-proxy-cache",

    "x-iinfo",

    "x-sucuri-id",

    "x-sucuri-cache",

    "x-hw",

    "x-vercel-cache",

    "x-vercel-id",

)

# ==========================================================
# Common Cache Headers
# ==========================================================

CACHE_HEADERS = (

    "cache-control",

    "age",

    "etag",

    "expires",

    "pragma",

    "last-modified",

    "vary",

)

# ==========================================================
# Default Analysis Result
# ==========================================================

EMPTY_RESULT = {

    "target": "",

    "cdn": False,

    "provider": "",

    "confidence": 0,

    "method": [],

    "headers": {},

    "server": "",

    "cname": "",

    "ip": "",

    "recommendations": [],

    "error": None,

}

# ==========================================================
# CDN Providers
# ==========================================================

CDN_PROVIDERS = (

    "Cloudflare",

    "Akamai",

    "Fastly",

    "Amazon CloudFront",

    "Azure Front Door",

    "Google Cloud CDN",

    "Imperva",

    "Sucuri",

    "StackPath",

    "BunnyCDN",

    "CDN77",

    "KeyCDN",

    "Leaseweb CDN",

    "G-Core",

    "Vercel",

    "Netlify",

    "QUIC.cloud",

    "Alibaba Cloud CDN",

    "Tencent Cloud CDN",

    "Oracle Cloud CDN",

)

# ==========================================================
# Header Fingerprints
# ==========================================================

HEADER_FINGERPRINTS = {

    # ------------------------------------------------------
    # Cloudflare
    # ------------------------------------------------------

    "Cloudflare": {

        "cf-ray",

        "cf-cache-status",

        "cf-request-id",

        "cf-worker",

        "cf-visitor",

        "nel",

        "report-to",

    },

    # ------------------------------------------------------
    # Akamai
    # ------------------------------------------------------

    "Akamai": {

        "akamai-origin-hop",

        "akamai-cache-status",

        "x-akamai-request-id",

        "x-akamai-session-info",

        "x-akamai-transformed",

    },

    # ------------------------------------------------------
    # Fastly
    # ------------------------------------------------------

    "Fastly": {

        "x-served-by",

        "x-cache-hits",

        "x-fastly-request-id",

        "fastly-debug-digest",

        "fastly-debug-path",

    },

    # ------------------------------------------------------
    # Amazon CloudFront
    # ------------------------------------------------------

    "Amazon CloudFront": {

        "x-amz-cf-id",

        "x-amz-cf-pop",

        "x-cache",

    },

    # ------------------------------------------------------
    # Azure Front Door
    # ------------------------------------------------------

    "Azure Front Door": {

        "x-azure-ref",

        "x-msedge-ref",

        "x-cache",

    },

    # ------------------------------------------------------
    # Google Cloud CDN
    # ------------------------------------------------------

    "Google Cloud CDN": {

        "via",

        "x-cache",

        "age",

        "alt-svc",

    },

    # ------------------------------------------------------
    # Imperva
    # ------------------------------------------------------

    "Imperva": {

        "x-iinfo",

        "x-cdn",

        "x-cdn-cache",

    },

    # ------------------------------------------------------
    # BunnyCDN
    # ------------------------------------------------------

    "BunnyCDN": {

        "cdn-pullzone",

        "cdn-requestcountrycode",

        "cdn-requestid",

    },


    # ------------------------------------------------------
    # CDN77
    # ------------------------------------------------------

    "CDN77": {

        "x-cdn",

        "x-cache",

        "x-cache-status",

        "x-edge-location",

    },

    # ------------------------------------------------------
    # KeyCDN
    # ------------------------------------------------------

    "KeyCDN": {

        "x-edge-location",

        "x-cache",

        "x-shield",

    },

    # ------------------------------------------------------
    # StackPath
    # ------------------------------------------------------

    "StackPath": {

        "x-sp-cache",

        "x-sp-edge",

        "x-cache",

    },

    # ------------------------------------------------------
    # Sucuri
    # ------------------------------------------------------

    "Sucuri": {

        "x-sucuri-id",

        "x-sucuri-cache",

        "x-sucuri-block",

    },

    # ------------------------------------------------------
    # Vercel
    # ------------------------------------------------------

    "Vercel": {

        "x-vercel-id",

        "x-vercel-cache",

        "x-vercel-ip-country",

    },

    # ------------------------------------------------------
    # Netlify
    # ------------------------------------------------------

    "Netlify": {

        "x-nf-request-id",

        "server-timing",

    },

    # ------------------------------------------------------
    # QUIC.cloud
    # ------------------------------------------------------

    "QUIC.cloud": {

        "x-qc-cache",

        "x-qc-pop",

        "x-qc-hit",

    },

    # ------------------------------------------------------
    # Leaseweb CDN
    # ------------------------------------------------------

    "Leaseweb CDN": {

        "x-lsw-cache",

        "x-cache",

    },

    # ------------------------------------------------------
    # G-Core
    # ------------------------------------------------------

    "G-Core": {

        "x-gcdn-cache",

        "x-gcore-cache",

    },

    # ------------------------------------------------------
    # Alibaba Cloud CDN
    # ------------------------------------------------------

    "Alibaba Cloud CDN": {

        "x-swift-cachetime",

        "eagleid",

        "x-cache",

    },

    # ------------------------------------------------------
    # Tencent Cloud CDN
    # ------------------------------------------------------

    "Tencent Cloud CDN": {

        "x-cache-lookup",

        "x-nws-log-uuid",

    },

    # ------------------------------------------------------
    # Oracle Cloud CDN
    # ------------------------------------------------------

    "Oracle Cloud CDN": {

        "opc-request-id",

        "x-cache",

    },

}

# ==========================================================
# Server Fingerprints
# ==========================================================

SERVER_FINGERPRINTS = {

    "cloudflare": "Cloudflare",

    "akamaighost": "Akamai",

    "akamai": "Akamai",

    "fastly": "Fastly",

    "cloudfront": "Amazon CloudFront",

    "amazon cloudfront": "Amazon CloudFront",

    "azure": "Azure Front Door",

    "azurefd": "Azure Front Door",

    "google": "Google Cloud CDN",

    "gws": "Google Cloud CDN",

    "imperva": "Imperva",

    "incapsula": "Imperva",

    "sucuri": "Sucuri",

    "stackpath": "StackPath",

    "bunnycdn": "BunnyCDN",

    "bunny": "BunnyCDN",

    "cdn77": "CDN77",

    "keycdn": "KeyCDN",

    "leaseweb": "Leaseweb CDN",

    "g-core": "G-Core",

    "gcore": "G-Core",

    "vercel": "Vercel",

    "netlify": "Netlify",

    "quic.cloud": "QUIC.cloud",

    "alibaba": "Alibaba Cloud CDN",

    "aliyun": "Alibaba Cloud CDN",

    "tencent": "Tencent Cloud CDN",

    "oracle": "Oracle Cloud CDN",

}

# ==========================================================
# CNAME Fingerprints
# ==========================================================

CNAME_FINGERPRINTS = {

    ".cloudflare.net": "Cloudflare",

    ".akamai.net": "Akamai",

    ".akamaiedge.net": "Akamai",

    ".edgekey.net": "Akamai",

    ".edgesuite.net": "Akamai",

    ".fastly.net": "Fastly",

    ".fastlylb.net": "Fastly",

    ".cloudfront.net": "Amazon CloudFront",

    ".azurefd.net": "Azure Front Door",

    ".trafficmanager.net": "Azure Front Door",

    ".googlehosted.com": "Google Cloud CDN",

    ".googleusercontent.com": "Google Cloud CDN",

    ".cdn.cloudflare.net": "Cloudflare",

    ".b-cdn.net": "BunnyCDN",

    ".cdn77.org": "CDN77",

    ".kxcdn.com": "KeyCDN",

    ".stackpathdns.com": "StackPath",

    ".netdna-cdn.com": "StackPath",

    ".sucuri.net": "Sucuri",

    ".incapdns.net": "Imperva",

    ".incapdns.com": "Imperva",

    ".vercel-dns.com": "Vercel",

    ".vercel.app": "Vercel",

    ".netlify.app": "Netlify",

    ".quic.cloud": "QUIC.cloud",

    ".lswcdn.net": "Leaseweb CDN",

    ".gcorelabs.net": "G-Core",

    ".gcdn.co": "G-Core",

    ".alicdn.com": "Alibaba Cloud CDN",

    ".tcdn.qq.com": "Tencent Cloud CDN",

    ".oraclecloud.net": "Oracle Cloud CDN",

}

# ==========================================================
# Cache Header Values
# ==========================================================

CACHE_PATTERNS = {

    "hit",

    "miss",

    "expired",

    "refresh",

    "dynamic",

    "static",

    "stale",

    "revalidated",

    "bypass",

}

# ==========================================================
# IP Provider Hints
# ==========================================================

IP_PROVIDER_HINTS = {

    "Cloudflare": (

        "104.16.",

        "104.17.",

        "104.18.",

        "104.19.",

        "172.64.",

        "188.114.",

    ),

    "Fastly": (

        "151.101.",

    ),

    "Amazon CloudFront": (

        "13.",

        "52.",

        "54.",

    ),

    "Google Cloud CDN": (

        "34.",

        "35.",

    ),

}

# ==========================================================
# Recommendations
# ==========================================================

RECOMMENDATIONS = {

    True:

        "A CDN was detected. Verify whether the provider "

        "matches the organization's expected infrastructure.",

    False:

        "No CDN fingerprints were detected. "

        "The origin server may be directly exposed.",

}

# ==========================================================
# Default Analysis
# ==========================================================

DEFAULT_ANALYSIS = {

    "target": "",

    "cdn": False,

    "provider": "",

    "confidence": UNKNOWN_CONFIDENCE,

    "method": [],

    "headers": {},

    "server": "",

    "cname": "",

    "ip": "",

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

    "DETECTED_FILE",

    "DEFAULT_HTTP_PORT",

    "DEFAULT_HTTPS_PORT",

    "DEFAULT_TIMEOUT",

    "MAX_REDIRECTS",

    "HIGH_CONFIDENCE",

    "MEDIUM_CONFIDENCE",

    "LOW_CONFIDENCE",

    "UNKNOWN_CONFIDENCE",

    "METHOD_HEADER",

    "METHOD_CNAME",

    "METHOD_SERVER",

    "METHOD_CACHE",

    "METHOD_DNS",

    "METHOD_IP",

    "METHOD_TLS",

    "DEFAULT_HEADERS",

    "COMMON_CDN_HEADERS",

    "CACHE_HEADERS",

    "EMPTY_RESULT",

    "CDN_PROVIDERS",

    "HEADER_FINGERPRINTS",

    "SERVER_FINGERPRINTS",

    "CNAME_FINGERPRINTS",

    "CACHE_PATTERNS",

    "IP_PROVIDER_HINTS",

    "RECOMMENDATIONS",

    "DEFAULT_ANALYSIS",

]

