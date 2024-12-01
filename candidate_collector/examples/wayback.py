import re
import logging
from pprint import pprint

from candidate_collector.builders import ExpandSymbolsPreprocessor
from candidate_collector.wayback import WaybackCollector
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.utils.helpers import load_qkeys
from candidate_collector.logging import configure_logging

def main():

    configure_logging()
    logger = logging.getLogger(__name__)

    domain = "9gag.com"
    keys = list(load_qkeys("indicators/prepared_qkeys.csv"))
    keys = ["to", "next", "url"]
    urls = set()

    key_subset = keys
    logger.info(f"Keys: {len(key_subset)}")

    pre_proc = ExpandSymbolsPreprocessor()
    pre_proc.expand("NUMBER", "\\d+")

    builder = RegexQueryBuilder(domain)
    builder.register_preprocessor(pre_proc)

    for key in key_subset:
        builder.require_query_key(key)
    regex = builder.build()

    logger.info(f"Regex: {regex}")

    wayback = WaybackCollector(domain, regex, limit=100, from_="2021", to="2023")
    logger.info(f"Query: {wayback.query()}")
    urls, _ = wayback.fetch()

    logger.info(f"URLs: {len(urls)}")

    with open(f"outputs/{domain}.txt", "w") as f:
        f.writelines([f"{url}\n" for url in urls])


if __name__ == "__main__":
    main()
