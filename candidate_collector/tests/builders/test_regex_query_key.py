import re
from or_collector.builders import RegexQueryBuilder
import pytest


class TestRegexQueryBuilderQueryKey:
    @pytest.fixture
    def query_regex(self):
        builder = RegexQueryBuilder("example.org")
        regex = (
            builder.require_query_key("url")
            .require_query_key("next")
            .exclude_query_key("q")
            .exclude_query_key("next-url")
            .require_query_value("https://example.org")
            .exclude_query_value("https")
            .require_query_pair("goto", "/accounts")
            .exclude_query_pair("goto", "https://example.org/accounts/login")
        ).build()
        return regex

    def test_require(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_query_key("url")).build()
        assert re.fullmatch(regex, "https://example.org") is None
        assert re.fullmatch(regex, "https://example.org?url") is not None
        assert re.fullmatch(regex, "https://example.org?url=value") is not None
        assert re.fullmatch(regex, "https://example.org?url=value=value") is not None
        assert re.fullmatch(regex, "https://example.org?foo=bar&url=value") is not None
        assert re.fullmatch(regex, "https://example.org?url=value&foo=bar") is not None

    def test_exlude(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.exclude_query_key("url")).build()
        assert re.fullmatch(regex, "https://example.org") is not None
        assert re.fullmatch(regex, "https://example.org?url") is None
        assert re.fullmatch(regex, "https://example.org?key=url") is not None
        assert re.fullmatch(regex, "https://example.org?url=value") is None
        assert re.fullmatch(regex, "https://example.org?url=value=value") is None
        assert re.fullmatch(regex, "https://example.org?foo=bar&url=value") is None
        assert re.fullmatch(regex, "https://example.org?url=value&foo=bar") is None

    def test_query(self, query_regex):
        assert re.fullmatch(query_regex, "https://example.org/") is None
        assert re.fullmatch(query_regex, "https://example.org/?") is None

        assert re.fullmatch(query_regex, "https://example.org?url") is not None
        assert re.fullmatch(query_regex, "https://example.org?url=") is not None
        assert re.fullmatch(query_regex, "https://example.org?url=value") is not None

        assert re.fullmatch(query_regex, "https://example.org?next") is not None
        assert re.fullmatch(query_regex, "https://example.org?next=") is not None
        assert re.fullmatch(query_regex, "https://example.org?next=value") is not None

        assert re.fullmatch(query_regex, "https://example.org?q") is None
        assert re.fullmatch(query_regex, "https://example.org?q=") is None
        assert re.fullmatch(query_regex, "https://example.org?q=value") is None

        assert re.fullmatch(query_regex, "https://example.org?next-url") is None
        assert re.fullmatch(query_regex, "https://example.org?next-url=") is None
        assert re.fullmatch(query_regex, "https://example.org?next-url=value") is None

        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&url") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&url=") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&url=value")
            is not None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next=") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next=value")
            is not None
        )

        assert re.fullmatch(query_regex, "https://example.org?key=value&q") is None
        assert re.fullmatch(query_regex, "https://example.org?key=value&q=") is None
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&q=value") is None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next-url") is None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next-url=") is None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?key=value&next-url=value")
            is None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?url&key=value") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?url=&key=value") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?url=value&key=value")
            is not None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?next&key=value") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?next=&key=value") is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?next=value&key=value")
            is not None
        )

        assert re.fullmatch(query_regex, "https://example.org?q&key=value") is None
        assert re.fullmatch(query_regex, "https://example.org?q=&key=value") is None
        assert (
            re.fullmatch(query_regex, "https://example.org?q=value&key=value") is None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?next-url&key=value") is None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?next-url=&key=value") is None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?next-url=value&key=value")
            is None
        )
