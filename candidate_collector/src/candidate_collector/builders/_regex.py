from ._base import QueryBuilder
from ._preprocess import EscapeREPreprocessor


class RegexQueryBuilder(QueryBuilder):
    def __init__(self, domain):
        super().__init__(domain)
        escape = EscapeREPreprocessor()
        self.register_preprocessor(escape)

    def build(self):
        scheme = self.build_scheme()
        domain = self.build_domain()

        path = self.build_path()
        query = self.build_query()

        path_quantifier = "?" if self.empty_path_allowed else ""
        query_quantifier = "?" if self.empty_query_allowed else ""

        return f"({scheme})({domain})(/{path}){path_quantifier}(\\?{query}){query_quantifier}"

    def build_scheme(self):
        return ".*//"

    def build_domain(self):
        regex = "[^/]*"
        if self.domain:
            regex = f"[^/]*?{self.domain}"
        return regex

    def build_path(self):
        required = self.build_path_required()
        excluded = self.build_path_excluded()
        regex = f"{excluded}{required}"
        return regex

    def build_path_required(self):
        """Either allows all or only the specified paths."""
        parts = [path for path in self.path_requirements]
        regex = ".*"
        if parts:
            regex = "|".join(parts)
            regex = f"(?:{regex})"
            trailing_slash = "(?:(?<!/)/)?" if self.ignore_trailing else ""
            regex = regex + trailing_slash
        return regex

    def build_path_excluded(self):
        """Either excludes nothing or only the specified paths."""
        parts = [path for path in self.path_excludes]
        regex = ""
        if parts:
            regex = "|".join(parts)
            suffix = "(?:\\?|$)"
            trailing_slash = "(?:(?<!/)/)?" if self.ignore_trailing else ""
            regex = f"(?!(?:{regex}{trailing_slash}{suffix}))"
        return regex

    def build_query(self):
        required = self.build_query_required()
        excluded = self.build_query_excluded()
        regex = f"{excluded}{required}"
        return regex

    def build_query_excluded(self):
        keys_excluded = self.build_keys_excluded()
        values_excluded = self.build_values_excluded()
        pairs_excluded = self.build_pairs_excluded()
        regex = ""
        if self.key_excludes or self.value_excludes or self.pair_excludes:
            regex = f"(?!.*{keys_excluded}{values_excluded}{pairs_excluded}.*)"
        return regex

    def build_query_required(self):
        keys_required = self.build_keys_required()
        values_required = self.build_values_required()
        pairs_required = self.build_pairs_required()
        parts = []
        if self.key_requirements:
            parts.append(keys_required)
        if self.value_requirements:
            parts.append(values_required)
        if self.pair_requirements:
            parts.append(pairs_required)
        regex = ".*"
        if parts:
            regex = "|".join(parts)
            regex = f"(.*(?:{regex}).*)"
        return regex

    def build_keys_required(self):
        """Either allows all or only the specified keys."""
        parts = [key for key in self.key_requirements]
        regex = ""
        if parts:
            regex = "|".join(parts)
            regex = f"(?<=&|\\?)(?:{regex})(?:=|&|$)"
        return regex

    def build_keys_excluded(self):
        """Either excludes nothing or only the specified keys."""
        parts = [key for key in self.key_excludes]
        regex = ""
        if parts:
            regex = "|".join(parts)
            regex = f"(?<=&|\\?)(?:{regex})(?:=|&|$)"
        return regex

    def build_values_required(self):
        """Either allows all or only the specified values."""
        parts = [value for value in self.value_requirements]
        regex = ""
        if parts:
            regex = "|".join(parts)
            regex = f"(?<==)(?:{regex})(?:&|$)"
        return regex

    def build_values_excluded(self):
        """Either excludes nothing or only the specified values."""
        parts = [value for value in self.value_excludes]
        regex = ""
        if parts:
            regex = "|".join(parts)
            regex = f"(?<==)(?:{regex})(?:&|$)"
        return regex

    def build_pairs_required(self):
        """Either allows all or only the specified pairs."""
        parts = [pair for pair in self.pair_requirements]
        regex = ""
        if parts:
            regex = "|".join([f"{key}={value}" for key, value in parts])
            regex = f"(?<=\\?|&)(?:{regex})(?:&|$)"
        return regex

    def build_pairs_excluded(self):
        """Either excludes nothing or only the specified pairs."""
        parts = [pair for pair in self.pair_excludes]
        regex = ""
        if parts:
            regex = "|".join([f"{key}={value}" for key, value in parts])
            regex = f"(?<=\\?|&)(?:{regex})(?:&|$)"
        return regex
