import re
from or_collector.builders import RegexQueryBuilder
import pytest


class TestRegexQueryBuilderPath:
    def test_path_trailing(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_path("users")).build()
        assert re.fullmatch(regex, "https://example.org/users") is not None
        assert re.fullmatch(regex, "https://example.org/users/") is None

    def test_path_trailing_slash(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_path("users/")).build()
        assert re.fullmatch(regex, "https://example.org/users") is None
        assert re.fullmatch(regex, "https://example.org/users/") is not None

    def test_path_trailing_discriminate(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.ignore_trailing_slash().require_path("users")).build()
        assert re.fullmatch(regex, "https://example.org/users") is not None
        assert re.fullmatch(regex, "https://example.org/users/") is not None

    def test_path_trailing_discriminate_slash(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.ignore_trailing_slash().require_path("users/")).build()
        assert re.fullmatch(regex, "https://example.org/users") is None
        assert re.fullmatch(regex, "https://example.org/users/") is not None
        assert re.fullmatch(regex, "https://example.org/users//") is None

    def test_path_leading_slash(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_path("/users")).build()
        assert re.fullmatch(regex, "https://example.org/users") is not None
        assert re.fullmatch(regex, "https://example.org//users") is None

    def test_path_required(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_path("/user")).build()
        assert re.fullmatch(regex, "https://example.org/user") is not None
        assert re.fullmatch(regex, "https://example.org/user-accounts") is None
        assert re.fullmatch(regex, "https://example.org/accounts-user") is None
        assert re.fullmatch(regex, "https://example.org/accounts/user") is None
        assert re.fullmatch(regex, "https://example.org/user/accounts") is None

    def test_path_excluded(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.exclude_path("/user")).build()
        assert re.fullmatch(regex, "https://example.org/user") is None
        assert re.fullmatch(regex, "https://example.org/user-accounts") is not None
        assert re.fullmatch(regex, "https://example.org/accounts-user") is not None
        assert re.fullmatch(regex, "https://example.org/accounts/user") is not None
        assert re.fullmatch(regex, "https://example.org/user/accounts") is not None

    def test_path_excluded_trailing(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.exclude_path("/user").ignore_trailing_slash()).build()
        assert re.fullmatch(regex, "https://example.org/user") is None
        assert re.fullmatch(regex, "https://example.org/user/") is None
        assert re.fullmatch(regex, "https://example.org/user-accounts") is not None
        assert re.fullmatch(regex, "https://example.org/accounts-user") is not None
        assert re.fullmatch(regex, "https://example.org/accounts/user") is not None
        assert re.fullmatch(regex, "https://example.org/user/accounts") is not None

    def test_path_required_exluded(self):
        builder = RegexQueryBuilder("example.org")
        regex = (
            builder.require_path("/user/details")
            .exclude_path("/user")
            .ignore_trailing_slash()
        ).build()
        assert re.fullmatch(regex, "https://example.org/user") is None
        assert re.fullmatch(regex, "https://example.org/user/details") is not None
        assert re.fullmatch(regex, "https://example.org/foo/user/details") is None
        assert re.fullmatch(regex, "https://example.org/user/details/foo") is None

    def test_path_exluded_required(self):
        builder = RegexQueryBuilder("example.org")
        regex = (
            builder.exclude_path("/user/details")
            .require_path("/user")
            .ignore_trailing_slash()
        ).build()
        assert re.fullmatch(regex, "https://example.org/user") is not None
        assert re.fullmatch(regex, "https://example.org/user/details") is None
        assert re.fullmatch(regex, "https://example.org/foo/user/details") is None
        assert re.fullmatch(regex, "https://example.org/user/details/foo") is None

    def test_path_domain_in_path_required(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.require_path("/example.org")).build()
        assert re.fullmatch(regex, "https://example.org") is None
        assert re.fullmatch(regex, "https://example.org/example.org") is not None
        assert re.fullmatch(regex, "https://example.org/foo/example.org") is None
        assert re.fullmatch(regex, "https://example.org/example.org/foo") is None

    def test_path_domain_in_path_excluded(self):
        builder = RegexQueryBuilder("example.org")
        regex = (builder.exclude_path("/example.org")).build()
        assert re.fullmatch(regex, "https://example.org") is not None
        assert re.fullmatch(regex, "https://example.org/example.org") is None
        assert re.fullmatch(regex, "https://example.org/foo/example.org") is not None
        assert re.fullmatch(regex, "https://example.org/example.org/foo") is not None

    @pytest.fixture
    def path_regex(self):
        builder = RegexQueryBuilder("example.org")
        regex = (
            builder.require_path("users")
            .require_path("accounts/login")
            .exclude_path("cats")
            .exclude_path("accounts")
        ).build()
        return regex

    def test_path(self, path_regex):

        assert re.fullmatch(path_regex, "https://example.org/unrelated") is None
        assert re.fullmatch(path_regex, "https://example.org/unrelated/") is None
        assert re.fullmatch(path_regex, "https://example.org/unrelated?") is None
        assert re.fullmatch(path_regex, "https://example.org/unrelated/?") is None

        assert (
            re.fullmatch(path_regex, "https://example.org/unrelated/accounts/login")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/unrelated/accounts/login/")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/unrelated/accounts/login/?")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/unrelated/acconts/login/?")
            is None
        )

        assert (
            re.fullmatch(path_regex, "https://example.org/accounts/login/unrelated")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/accounts/login/unrelated/")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/accounts/login/unrelated/?")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/acconts/login/unrelated/?")
            is None
        )

        assert re.fullmatch(path_regex, "https://example.org") is None
        assert re.fullmatch(path_regex, "https://example.org/") is None
        assert re.fullmatch(path_regex, "https://example.org?") is None
        assert re.fullmatch(path_regex, "https://example.org/?") is None

        assert re.fullmatch(path_regex, "https://example.org/cats") is None
        assert re.fullmatch(path_regex, "https://example.org/cats/") is None
        assert re.fullmatch(path_regex, "https://example.org/cats?") is None
        assert re.fullmatch(path_regex, "https://example.org/cats/?") is None

        assert re.fullmatch(path_regex, "https://example.org/accounts") is None
        assert re.fullmatch(path_regex, "https://example.org/accounts/") is None
        assert re.fullmatch(path_regex, "https://example.org/accounts?") is None
        assert re.fullmatch(path_regex, "https://example.org/accounts/?") is None

        assert re.fullmatch(path_regex, "https://example.org/users") is not None
        assert re.fullmatch(path_regex, "https://example.org/users/") is None
        assert re.fullmatch(path_regex, "https://example.org/users?") is not None
        assert re.fullmatch(path_regex, "https://example.org/users/?") is None

        assert (
            re.fullmatch(path_regex, "https://example.org/users/accounts/login") is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/users/accounts/login/")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/users/accounts/login/?")
            is None
        )
        assert (
            re.fullmatch(path_regex, "https://example.org/users/accounts/login/?")
            is None
        )

        assert re.fullmatch(path_regex, "https://example.org//users") is None
        assert re.fullmatch(path_regex, "https://example.org//users/") is None
        assert re.fullmatch(path_regex, "https://example.org//users?") is None
        assert re.fullmatch(path_regex, "https://example.org//users/?") is None
