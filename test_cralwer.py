from modules.crawler.crawler import crawl_host
from pprint import pprint

result = crawl_host(
    "https://httpbin.org"
)

pprint(result)