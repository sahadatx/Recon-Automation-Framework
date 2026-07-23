"""
CDN Manager Test
"""

from unittest.mock import patch

from modules.cdn.manager import run_cdn_detection


PASSED = 0
FAILED = 0


def run_test(
    name: str,
    condition: bool,
) -> None:
    """
    Print test result.
    """

    global PASSED
    global FAILED

    if condition:

        PASSED += 1

        print(f"[PASS] {name}")

    else:

        FAILED += 1

        print(f"[FAIL] {name}")


print("=" * 60)
print("CDN MANAGER TEST")
print("=" * 60)


MOCK_RESULT = {

    "target": "example.com",

    "cdn": True,

    "provider": "Cloudflare",

    "confidence": 95,

    "method": [

        "Header",

    ],

    "headers": {},

    "cname": "example.cloudflare.net",

    "ip": "104.16.0.1",

    "recommendations": [],

}


MOCK_STATISTICS = {

    "targets": 1,

    "detected": 1,

    "undetected": 0,

    "average_confidence": 95,

    "highest_confidence": 95,

    "elapsed": 0.01,

    "provider_statistics": {

        "Cloudflare": 1,

    },

    "confidence_statistics": {

        "high": 1,

        "medium": 0,

        "low": 0,

        "unknown": 0,

    },

}


try:

    with (

        patch(

            "modules.cdn.manager.normalize_target",

            return_value="example.com",

        ),

        patch(

            "modules.cdn.manager.request_headers",

            return_value=object(),

        ),

        patch(

            "modules.cdn.manager.extract_headers",

            return_value={},

        ),

        patch(

            "modules.cdn.manager.resolve_cname",

            return_value="example.cloudflare.net",

        ),

        patch(

            "modules.cdn.manager.resolve_ipv4",

            return_value="104.16.0.1",

        ),

        patch(

            "modules.cdn.manager.analyze",

            return_value=MOCK_RESULT,

        ),

        patch(

            "modules.cdn.manager.filter_results",

            return_value=[MOCK_RESULT],

        ),

        patch(

            "modules.cdn.manager.generate_statistics",

            return_value=MOCK_STATISTICS,

        ),

        patch(

            "modules.cdn.manager.export_results",

        ),

        patch(

            "modules.cdn.manager.print_summary",

        ),

    ):

        results, statistics = run_cdn_detection(

            [

                "https://example.com",

            ]

        )

    success = (

        len(results) == 1

        and statistics["targets"] == 1

        and results[0]["provider"] == "Cloudflare"

    )

except Exception as error:

    print(error)

    success = False


run_test(

    "Run CDN Detection",

    success,

)


print("=" * 60)
print(f"Passed : {PASSED}")
print(f"Failed : {FAILED}")
print("=" * 60)