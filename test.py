from pprint import pprint

from modules.fuzzing.manager import run_fuzzing

pprint(
    run_fuzzing(
        [
            "https://testphp.vulnweb.com",
        ]
    )
)