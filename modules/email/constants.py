"""
Email Security Constants

Centralized constants used by the
Email Security module.
"""

from __future__ import annotations

from pathlib import Path

from config.config import (

    DNS_TIMEOUT,

)

# ==========================================================
# Output Directory
# ==========================================================

OUTPUT_DIR = Path(

    "output/email",

)

OUTPUT_DIR.mkdir(

    parents=True,

    exist_ok=True,

)

TXT_FILE = OUTPUT_DIR / "results.txt"

JSON_FILE = OUTPUT_DIR / "results.json"

CSV_FILE = OUTPUT_DIR / "results.csv"

SUMMARY_FILE = OUTPUT_DIR / "summary.txt"

HIGH_RISK_FILE = OUTPUT_DIR / "high_risk.txt"

# ==========================================================
# Network Defaults
# ==========================================================

DEFAULT_TIMEOUT = DNS_TIMEOUT

# ==========================================================
# Risk Levels
# ==========================================================

LOW_RISK = "Low"

MEDIUM_RISK = "Medium"

HIGH_RISK = "High"

CRITICAL_RISK = "Critical"

# ==========================================================
# Risk Score Thresholds
# ==========================================================

LOW_SCORE = 20

MEDIUM_SCORE = 40

HIGH_SCORE = 60

# ==========================================================
# DNS Record Types
# ==========================================================

MX_RECORD = "MX"

TXT_RECORD = "TXT"

DNSKEY_RECORD = "DNSKEY"

# ==========================================================
# Default Analysis Result
# ==========================================================

EMPTY_RESULT = {

    "target": "",

    "mx": [],

    "provider": "",

    "spf": False,

    "spf_record": "",

    "dkim": False,

    "dkim_selector": "",

    "dmarc": False,

    "dmarc_record": "",

    "mta_sts": False,

    "tls_rpt": False,

    "bimi": False,

    "dnssec": False,

    "score": 0,

    "risk": LOW_RISK,

    "recommendations": [],

    "error": None,

}


# ==========================================================
# Mail Providers
# ==========================================================

MAIL_PROVIDERS = {

    "Google Workspace": (

        ".google.com",

        ".googlemail.com",

        ".l.google.com",

    ),

    "Microsoft 365": (

        ".outlook.com",

        ".protection.outlook.com",

    ),

    "Zoho Mail": (

        ".zoho.com",

    ),

    "Proton Mail": (

        ".protonmail.ch",

        ".protonmail.net",

    ),

    "Fastmail": (

        ".messagingengine.com",

    ),

    "Amazon SES": (

        ".amazonses.com",

    ),

    "Mailgun": (

        ".mailgun.org",

    ),

    "SendGrid": (

        ".sendgrid.net",

    ),

    "Proofpoint": (

        ".pphosted.com",

    ),

    "Mimecast": (

        ".mimecast.com",

    ),

    "Cisco ESA": (

        ".iphmx.com",

    ),

    "Barracuda": (

        ".ess.barracudanetworks.com",

    ),

}

# ==========================================================
# Common DKIM Selectors
# ==========================================================

DKIM_SELECTORS = (

    "default",

    "google",

    "selector1",

    "selector2",

    "k1",

    "mail",

)

# ==========================================================
# DNS Prefixes
# ==========================================================

DMARC_PREFIX = "_dmarc"

MTA_STS_PREFIX = "_mta-sts"

TLS_RPT_PREFIX = "_smtp._tls"

BIMI_PREFIX = "default._bimi"

# ==========================================================
# Recommendations
# ==========================================================

RECOMMENDATIONS = {

    True: [

        "Review missing email security records.",

        "Configure SPF, DKIM and DMARC.",

        "Enable MTA-STS and TLS Reporting.",

        "Consider enabling BIMI and DNSSEC.",

    ],

    False: [

        "Email security configuration looks healthy.",

    ],

}

# ==========================================================
# Export Fields
# ==========================================================

EXPORT_FIELDS = (

    "target",

    "provider",

    "spf",

    "dkim",

    "dmarc",

    "mta_sts",

    "tls_rpt",

    "bimi",

    "dnssec",

    "score",

    "risk",

)

# ==========================================================
# Default Analysis
# ==========================================================

DEFAULT_ANALYSIS = {

    "target": "",

    "mx": [],

    "provider": "",

    "spf": False,

    "spf_record": "",

    "dkim": False,

    "dkim_selector": "",

    "dmarc": False,

    "dmarc_record": "",

    "mta_sts": False,

    "tls_rpt": False,

    "bimi": False,

    "dnssec": False,

    "score": 0,

    "risk": LOW_RISK,

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

    "HIGH_RISK_FILE",

    "DEFAULT_TIMEOUT",

    "LOW_RISK",

    "MEDIUM_RISK",

    "HIGH_RISK",

    "CRITICAL_RISK",

    "LOW_SCORE",

    "MEDIUM_SCORE",

    "HIGH_SCORE",

    "MX_RECORD",

    "TXT_RECORD",

    "DNSKEY_RECORD",

    "EMPTY_RESULT",

    "MAIL_PROVIDERS",

    "DKIM_SELECTORS",

    "DMARC_PREFIX",

    "MTA_STS_PREFIX",

    "TLS_RPT_PREFIX",

    "BIMI_PREFIX",

    "RECOMMENDATIONS",

    "EXPORT_FIELDS",

    "DEFAULT_ANALYSIS",

]

