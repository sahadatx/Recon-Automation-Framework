import re


SECRET_PATTERNS = {


    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "aws_secret_key": re.compile(r"\b[A-Za-z0-9/+=]{40}\b"),


    "google_api_key": re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b"),


    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),


    "gitlab_token": re.compile(r"\bglpat-[A-Za-z0-9\-_]{20,255}\b"),


    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,200}\b"),


    "stripe_live_key": re.compile(r"\bsk_live_[A-Za-z0-9]{24,}\b"),
    "stripe_test_key": re.compile(r"\bsk_test_[A-Za-z0-9]{24,}\b"),


    "firebase_key": re.compile(r"\bAAAA[A-Za-z0-9_-]{7,}\b"),


    "twilio_sid": re.compile(r"\bAC[a-fA-F0-9]{32}\b"),


    "openai_key": re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"),


    "jwt": re.compile(
        r"\beyJ[A-Za-z0-9_\-]+" r"\.[A-Za-z0-9_\-]+" r"\.[A-Za-z0-9_\-]+\b"
    ),


    "bearer_token": re.compile(
        r"Bearer\s+[A-Za-z0-9\-._~+/]+=*",
        re.IGNORECASE,
    ),


    "basic_auth": re.compile(
        r"Basic\s+[A-Za-z0-9+/=]+",
        re.IGNORECASE,
    ),


    "rsa_private_key": re.compile(
        r"-----BEGIN RSA PRIVATE KEY-----" r".*?" r"-----END RSA PRIVATE KEY-----",
        re.DOTALL,
    ),


    "private_key": re.compile(
        r"-----BEGIN PRIVATE KEY-----" r".*?" r"-----END PRIVATE KEY-----",
        re.DOTALL,
    ),


    "ec_private_key": re.compile(
        r"-----BEGIN EC PRIVATE KEY-----" r".*?" r"-----END EC PRIVATE KEY-----",
        re.DOTALL,
    ),


    "openssh_private_key": re.compile(
        r"-----BEGIN OPENSSH PRIVATE KEY-----"
        r".*?"
        r"-----END OPENSSH PRIVATE KEY-----",
        re.DOTALL,
    ),


    "generic_api_key": re.compile(
        r"""(?i)
        (?:api[_-]?key|
           secret|
           access[_-]?key|
           auth[_-]?token)
        \s*
        [:=]
        \s*
        ['"]?
        ([A-Za-z0-9_\-]{16,})
        ['"]?
        """,
        re.VERBOSE,
    ),
}


SUPPORTED_SECRETS = tuple(SECRET_PATTERNS.keys())
