import logging
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.builders import ExpandSymbolsPreprocessor
from candidate_collector.logging import configure_logging

def main():

    configure_logging()
    logger = logging.getLogger()


    domain = "example.org"
    pre_proc = ExpandSymbolsPreprocessor()
    pre_proc.expand("ANY", ".*")

    builder = RegexQueryBuilder(domain)
    builder.register_preprocessor(pre_proc)

    regex = (
        builder.ignore_trailing_slash()
        .require_query_value("/ANY")
        .require_query_value("httpANY")
        .require_query_key("next")
        .require_query_key("redirect")
    ).build()
    logger.info(f"Regex: {regex}")


if __name__ == "__main__":
    main()
