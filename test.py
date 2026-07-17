"""
Test WAF Detection Module
"""

from modules.waf.manager import run


TARGETS = [

    # Cloudflare
    "https://cloudflare.com",

    # AWS
    "https://aws.amazon.com",

    # Azure
    "https://azure.microsoft.com",

    # Fastly
    "https://www.fastly.com",

    # Imperva
    "https://www.imperva.com",

    # Akamai
    "https://www.akamai.com",

    # Sucuri
    "https://sucuri.net",

    # Fortinet
    "https://www.fortinet.com",

    # TestFire
    "https://demo.testfire.net",

    # No WAF (example target)
    "https://example.com",

]


def main():

    run(

        TARGETS

    )


if __name__ == "__main__":

    main()