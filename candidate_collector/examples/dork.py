import os
import logging

from dotenv import load_dotenv

from pprint import pprint

from candidate_collector.dork import DorkCollector
from candidate_collector.builders import DorkQueryBuilder
from candidate_collector.logging import configure_logging


def load_qkeys():
    qkeys = []
    with open("indicators/prepared_qkeys.csv", "r") as param_file:
        qkeys = param_file.read().splitlines()
    return qkeys



def main():

    load_dotenv()
    configure_logging()
    api_key = os.environ.get("GOOGLE_API_KEY")
    se_id = os.environ.get("GOOGLE_SE_ID")
    logger = logging.getLogger(__name__)

    domain = "linkedin.com"
    keys = load_qkeys()
    urls = set()

    logger.info(f"Keys: {len(keys)}")

    builder = DorkQueryBuilder(domain)

    for key in keys:
        builder.require_query_key(key)
    dork_query = builder.build()

    dork_query = f'site:{domain} inurl:%3a%2f%2f'
    logger.info(f"Dork query: {dork_query}")
    logger.info(f"Dork query length: {len(dork_query)}")

    dork = DorkCollector(dork_query, api_key, se_id)
    data = dork.fetch()
    urls = DorkCollector.extract_urls(data)

    logger.info(f"URLs: {len(urls)}")
    for url in urls:
        logger.info(url)

    with open(f"outputs/{domain}.txt", "w") as f:
        f.writelines([f"{url}\n" for url in urls])


if __name__ == "__main__":
    main()
