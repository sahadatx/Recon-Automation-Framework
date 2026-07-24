"""
Screenshot Module Test

Integration test for Screenshot Engine.
"""


from modules.screenshots.manager import (
    execute,
)



# ==========================================================
# Main Test
# ==========================================================

def main():


    http_results = {

        "example.com": {

            "url":
                "https://example.com",

            "status":
                200,

        },

    }


    print(
        "=" * 70
    )

    print(
        "Screenshot Module Integration Test"
    )

    print(
        "=" * 70
    )


    analysis = execute(

        http_results

    )


    print()


    print(
        "=" * 70
    )

    print(
        "TEST RESULT"
    )

    print(
        "=" * 70
    )


    print(
        "Type:",
        type(analysis)
    )


    print(
        "Keys:",
        list(
            analysis.keys()
        )
    )


    print()


    print(
        "Total Targets:",
        analysis.get(
            "total_targets"
        )
    )


    print(
        "Captured:",
        analysis.get(
            "captured"
        )
    )


    print(
        "Failed:",
        analysis.get(
            "failed"
        )
    )


    print(
        "Scan Time:",
        analysis.get(
            "scan_time"
        )
    )


    print()


    print(
        "Screenshots:"
    )


    print(
        "-" * 70
    )


    for item in analysis.get(

        "results",

        []

    ):


        print(
            "URL:",
            item.get(
                "url"
            )
        )


        print(
            "Captured:",
            item.get(
                "captured"
            )
        )


        print(
            "Status:",
            item.get(
                "status"
            )
        )


        print(
            "Image:",
            item.get(
                "path"
            )
        )


        print(
            "-" * 70
        )


    print()

    print(
        "Done."
    )



# ==========================================================
# Entry
# ==========================================================

if __name__ == "__main__":

    main()