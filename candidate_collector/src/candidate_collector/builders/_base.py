from abc import ABC, abstractmethod
from ._exceptions import BuilderError


class QueryBuilder(ABC):
    def __init__(self, domain):
        self.domain = ""
        self.empty_path_allowed = True
        self.empty_query_allowed = True
        self.ignore_trailing = False

        self.path_requirements = set()
        self.path_excludes = set()

        self.key_requirements = set()
        self.key_excludes = set()

        self.value_requirements = set()
        self.value_excludes = set()

        self.pair_requirements = set()
        self.pair_excludes = set()

        self.preprocessors = list()

        self.require_domain(domain)

    def register_preprocessor(self, preprocessor):
        self.preprocessors.append(preprocessor)

    def preprocess(self, value):
        res = value
        for preprocessor in self.preprocessors:
            res = preprocessor.process(value)
        return res

    @abstractmethod
    def build(self):
        """Build query based on the current state of the builder."""
        pass

    def disallow_empty_path(self):
        self.empty_path_allowed = False
        return self

    def disallow_empty_query(self):
        self.empty_query_allowed = False
        return self

    def ignore_trailing_slash(self):
        self.ignore_trailing = True
        return self

    def require_domain(self, domain):
        """Tells the builder to check for specified domain."""
        if self.domain:
            raise BuilderError("Domain already specified")
        self.domain = self.preprocess(domain)
        return self

    def require_path(self, path):
        """Tells the builder to require the specified path."""
        """ Removes leading slashes. """
        path = path.lstrip("/")
        if path in self.path_excludes:
            raise BuilderError(f"Conflict! The path is already explicitly excluded.")
        if not path:
            raise BuilderError(f"Invalid path! Path must not be empty.")
        path = self.preprocess(path)
        self.path_requirements.add(path)
        self.disallow_empty_path()
        return self

    def exclude_path(self, path):
        """Tells the builder to exclude the specified path."""
        """ Removes leading slashes. """
        path = path.lstrip("/")
        if path in self.path_requirements:
            raise BuilderError(f"Conflict! The path is already explicitly included.")
        if not path:
            raise BuilderError(f"Invalid path! Path must not be empty.")
        path = self.preprocess(path)
        self.path_excludes.add(path)
        return self

    def require_query_key(self, key):
        """Tells the builder to require the specified query key."""
        if key in self.key_excludes:
            raise BuilderError(f"Conflict! The path is already explicitly excluded.")
        key = self.preprocess(key)
        self.key_requirements.add(key)
        self.disallow_empty_query()
        return self

    def exclude_query_key(self, key):
        """Tells the builder to exclude the specified query key."""
        if key in self.key_requirements:
            raise BuilderError(f"Conflict! The path is already explicitly included.")
        key = self.preprocess(key)
        self.key_excludes.add(key)
        return self

    def require_query_value(self, value):
        """Tells the builder to require the specified query value."""
        if value in self.value_excludes:
            raise BuilderError(f"Conflict! The value is already explicitly excluded.")
        value = self.preprocess(value)
        self.value_requirements.add(value)
        self.disallow_empty_query()
        return self

    def exclude_query_value(self, value):
        """Tells the builder to exclude the specified query value."""
        if value in self.value_requirements:
            raise BuilderError(f"Conflict! The value is already explicitly excluded.")
        value = self.preprocess(value)
        self.value_excludes.add(value)
        return self

    def require_query_pair(self, key, value):
        """Tells the builder to require the specified query pair."""
        if any([key == k and value == v for k, v in self.pair_excludes]):
            raise BuilderError(f"Conflict! The pair is already explicitly excluded.")
        key = self.preprocess(key)
        value = self.preprocess(value)
        self.pair_requirements.add((key, value))
        self.disallow_empty_query()
        return self

    def exclude_query_pair(self, key, value):
        """Tells the builder to exclude the specified query pair."""
        if any([key == k and value == v for k, v in self.pair_requirements]):
            raise BuilderError(f"Conflict! The pair is already explicitly excluded.")
        key = self.preprocess(key)
        value = self.preprocess(value)
        self.pair_excludes.add((key, value))
        return self
