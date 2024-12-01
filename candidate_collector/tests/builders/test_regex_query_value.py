import re
from or_collector.builders import RegexQueryBuilder
import pytest


class TestRegexQueryBuilderQueryValue:
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

    def test_query(self, query_regex):
        assert (
            re.fullmatch(query_regex, "https://example.org?https://example.org") is None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?foo=https://example.org")
            is not None
        )
        assert re.fullmatch(query_regex, "https://example.org?foo=https") is None

        assert (
            re.fullmatch(query_regex, "https://example.org?q=https://example.org")
            is not None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?foo=Xhttps://example.org")
            is None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?foo=https://example.orgX")
            is None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org?url=Xhttps://example.org")
            is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org?next=https://example.orgX")
            is not None
        )

        assert re.fullmatch(query_regex, "https://example.org?foo=bar") is None

        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?foo=https://example.org"
            )
            is not None
        )
        assert (
            re.fullmatch(query_regex, "https://example.org/some/path/?foo=https")
            is None
        )

        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?q=https://example.org"
            )
            is not None
        )

        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?foo=Xhttps://example.org"
            )
            is None
        )
        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?foo=https://example.orgX"
            )
            is None
        )

        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?url=Xhttps://example.org"
            )
            is not None
        )
        assert (
            re.fullmatch(
                query_regex, "https://example.org/some/path/?next=https://example.orgX"
            )
            is not None
        )

        assert (
            re.fullmatch(query_regex, "https://example.org/some/path/?foo=bar") is None
        )
