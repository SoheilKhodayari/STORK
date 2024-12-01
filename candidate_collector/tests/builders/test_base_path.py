import pytest
from or_collector.builders import QueryBuilder
from or_collector.builders import BuilderError


class NOPQueryBuilder(QueryBuilder):
    def build(self):
        return None


class TestBaseQueryBuilderPath:
    @pytest.fixture
    def builder(self):
        return NOPQueryBuilder("example.org")

    def test_path_conflict_require(self, builder):
        with pytest.raises(BuilderError):
            builder.require_path("foo")
            builder.exclude_path("foo")

    def test_path_conflict_exclude(self, builder):
        with pytest.raises(BuilderError):
            builder.exclude_path("foo")
            builder.require_path("foo")

    def test_path_conflict_require_complex_1(self, builder):
        builder.require_path("foo/bar")
        builder.exclude_path("foo")

    def test_path_conflict_exclude_complex_1(self, builder):
        builder.exclude_path("foo/bar")
        builder.require_path("foo")

    def test_path_conflict_require_complex_2(self, builder):
        builder.require_path("foo/bar")
        builder.exclude_path("bar")

    def test_path_conflict_exclude_complex_2(self, builder):
        builder.exclude_path("foo/bar")
        builder.require_path("bar")

    def test_path_require_complex(self, builder):
        builder.require_path("foo")
        builder.exclude_path("foo/bar")

    def test_path_excluede_complex(self, builder):
        builder.require_path("foo")
        builder.exclude_path("foo/bar")
