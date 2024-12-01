import pytest
from or_collector.builders import QueryBuilder
from or_collector.builders import BuilderError


class NOPQueryBuilder(QueryBuilder):
    def build(self):
        return None


class TestBaseQueryBuilderQuery:
    @pytest.fixture
    def builder(self):
        return NOPQueryBuilder("example.org")

    #######################
    # Query Parameter Key #
    #######################

    def test_key_conflict_require(self, builder):
        with pytest.raises(BuilderError):
            builder.require_query_key("foo")
            builder.exclude_query_key("foo")

    def test_key_conflict_exclude(self, builder):
        with pytest.raises(BuilderError):
            builder.exclude_query_key("foo")
            builder.require_query_key("foo")

    def test_key_conflict_require_benign_1(self, builder):
        builder.require_query_key("fooXbar")
        builder.exclude_query_key("foo")

    def test_key_conflict_exclude_benign_1(self, builder):
        builder.exclude_query_key("fooXbar")
        builder.require_query_key("foo")

    def test_key_conflict_require_benign_2(self, builder):
        builder.require_query_key("fooXbar")
        builder.exclude_query_key("bar")

    def test_key_conflict_exclude_benign_2(self, builder):
        builder.exclude_query_key("fooXbar")
        builder.require_query_key("bar")

    #########################
    # Query Parameter Value #
    #########################

    def test_value_conflict_require(self, builder):
        with pytest.raises(BuilderError):
            builder.require_query_value("foo")
            builder.exclude_query_value("foo")

    def test_value_conflict_exclude(self, builder):
        with pytest.raises(BuilderError):
            builder.exclude_query_value("foo")
            builder.require_query_value("foo")

    def test_value_conflict_require_complex_1(self, builder):
        builder.require_query_value("fooXbar")
        builder.exclude_query_value("foo")

    def test_value_conflict_exclude_complex_1(self, builder):
        builder.exclude_query_value("fooXbar")
        builder.require_query_value("foo")

    def test_value_conflict_require_complex_2(self, builder):
        builder.require_query_value("fooXbar")
        builder.exclude_query_value("bar")

    def test_value_conflict_exclude_complex_2(self, builder):
        builder.exclude_query_value("fooXbar")
        builder.require_query_value("bar")

    #########################
    # Query Parameter Pair  #
    #########################

    def test_pair_conflict_require(self, builder):
        with pytest.raises(BuilderError):
            builder.require_query_pair("key", "value")
            builder.exclude_query_pair("key", "value")

    def test_pair_conflict_exclude(self, builder):
        with pytest.raises(BuilderError):
            builder.exclude_query_pair("key", "value")
            builder.require_query_pair("key", "value")

    def test_pair_conflict_require_complex_1(self, builder):
        builder.require_query_pair("key", "fooXbar")
        builder.exclude_query_pair("key", "foo")

    def test_pair_conflict_exclude_complex_1(self, builder):
        builder.exclude_query_pair("key", "fooXbar")
        builder.require_query_pair("key", "foo")

    def test_pair_conflict_require_complex_2(self, builder):
        builder.require_query_pair("key", "fooXbar")
        builder.exclude_query_pair("key", "bar")

    def test_pair_conflict_exclude_complex_2(self, builder):
        builder.exclude_query_pair("key", "fooXbar")
        builder.require_query_pair("key", "bar")

    def test_pair_conflict_require_complex_3(self, builder):
        builder.require_query_pair("key1", "fooXbar")
        builder.exclude_query_pair("key2", "X")

    def test_pair_conflict_exclude_complex_3(self, builder):
        builder.exclude_query_pair("key1", "fooXbar")
        builder.require_query_pair("key2", "X")
