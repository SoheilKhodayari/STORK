import logging
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.builders import ExpandSymbolsPreprocessor
from candidate_collector.logging import configure_logging

def main():

    configure_logging()
    logger = logging.getLogger(__name__)

    pre_proc = ExpandSymbolsPreprocessor()
    pre_proc.expand("NUMBER", "\\d+")

    builder = RegexQueryBuilder("example.org")
    builder.register_preprocessor(pre_proc)

    regex = (
        builder
        .require_path("accounts/register")
        .require_path("users/NUMBER/")
        .exclude_path("users")
        .require_query_pair("number", "NUMBER")
        .require_query_key("url")
        .require_query_pair("foo", "bar")
        .require_query_key("baz")
    ).build()
    logger.info(f"Regex: {regex}")


if __name__ == "__main__":
    main()
