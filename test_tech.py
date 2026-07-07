from pprint import pprint

from modules.tech.manager import (
    detect_hosts,
)

responses = {

    "google.com": {

        "url": "https://google.com",

        "server": "gws",

        "headers": {

            "Server": "gws",

        },

        "html": "<html></html>",

    },

    "github.com": {

        "url": "https://github.com",

        "server": "GitHub",

        "headers": {

            "Server": "GitHub",

            "X-Powered-By": "Rails",

        },

        "html": """

        <html>

        wp-content

        </html>

        """,

    },

}

results, failed, elapsed = detect_hosts(
    responses
)

pprint(results)

print(failed)

print(elapsed)