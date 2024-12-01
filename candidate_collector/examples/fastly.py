import re
import logging

from candidate_collector.builders import ExpandSymbolsPreprocessor
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.utils.helpers import load_qkeys
from candidate_collector.logging import configure_logging


def load_urls():
    with open("data/fastly.csv", "r") as f:
        urls = f.read().splitlines()
        return urls


def main():

    configure_logging()
    logger = logging.getLogger(__name__)

    domain = "fastly.net"
    keys = list(load_qkeys("data/parameters.txt"))
    urls = load_urls()
    unmatched_urls = set()
    matched_urls = set()

    key_subset = keys
    logger.info(f"Keys: {len(key_subset)}")
    logger.info(f"URLs: {len(urls)}")

    pre_proc = ExpandSymbolsPreprocessor()
    pre_proc.expand("NUMBER", "\\d+")

    builder = RegexQueryBuilder(domain)
    builder.register_preprocessor(pre_proc)

    for key in key_subset:
        builder.require_query_key(key)
    regex = builder.build()

    logger.info(f"Regex: {regex}")

    for url in urls:
        if re.search(regex, url) is None:
            unmatched_urls.add(url)
        else:
            matched_urls.add(url)

    logger.info(f"Unmatched URLs: {len(unmatched_urls)}")
    logger.info(f"Unmatched URLs: {len(matched_urls)}")


if __name__ == "__main__":
    main()
