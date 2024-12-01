import re
from or_collector.builders import RegexQueryBuilder
import pytest


class TestRegexQueryBuilderDomain:
    @pytest.fixture
    def domain_regex(self):
        builder = RegexQueryBuilder("example.org")
        regex = builder.build()
        return regex

    def test_domain(self, domain_regex):
        assert re.fullmatch(domain_regex, "https://example.org") is not None
        assert (
            re.fullmatch(domain_regex, "https://unrelated.test@example.org") is not None
        )
        assert (
            re.fullmatch(domain_regex, "https://user:password@example.org") is not None
        )
        assert re.fullmatch(domain_regex, "https://www.example.org") is not None

        assert re.fullmatch(domain_regex, "https://example.org/") is not None
        assert (
            re.fullmatch(domain_regex, "https://unrelated.test@example.org/")
            is not None
        )
        assert (
            re.fullmatch(domain_regex, "https://user:password@example.org/") is not None
        )
        assert re.fullmatch(domain_regex, "https://www.example.org/") is not None

        assert re.fullmatch(domain_regex, "https://example.org/?") is not None
        assert (
            re.fullmatch(domain_regex, "https://unrelated.test@example.org/?")
            is not None
        )
        assert (
            re.fullmatch(domain_regex, "https://user:password@example.org/?")
            is not None
        )
        assert re.fullmatch(domain_regex, "https://www.example.org/?") is not None

        assert re.fullmatch(domain_regex, "https://example.org@unrelated.test") is None
