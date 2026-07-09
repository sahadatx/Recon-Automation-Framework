from pprint import pprint

from modules.nuclei.scanner import scan_target
from modules.nuclei.parser import parse_nuclei

result = scan_target(
    "https://demo.testfire.net",
    profile="fast",
)

pprint(result)

if result["success"]:

    print("\nOutput File:")
    print(result["output"])

    print("\nParsed:")
    pprint(
        parse_nuclei(result["output"])
    )