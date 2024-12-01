from abc import ABC, abstractmethod
from urllib.parse import parse_qsl, urlparse


class Heuristic(ABC):

    @abstractmethod
    def evaluate(self, url):
        pass

    def get_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.get_name()

class QueryKeyHeuristic(Heuristic):

    def __init__(self, vuln_query_keys):
        self.vuln_query_keys = vuln_query_keys
    
    def evaluate(self, url):
        parsed_url = urlparse(url)
        parsed_qsl = parse_qsl(parsed_url.query, keep_blank_values=True)
        for qkey, _ in parsed_qsl:
            if qkey in self.vuln_query_keys:
                return True
        return False

class QueryKeyPathValueHeuristic(Heuristic):

    def __init__(self, vuln_query_keys):
        self.vuln_query_keys = vuln_query_keys

    def evaluate(self, url):
        parsed_url = urlparse(url)
        parsed_qsl = parse_qsl(parsed_url.query)
        for qkey, qval in parsed_qsl:
            if (qkey in self.vuln_query_keys and (
                qval.startswith("%2f")
                or qval.startswith("%2F")
                or qval.startswith("/"))):
                return True
        return False

class QueryKeyURLValueHeuristic(Heuristic):

    def __init__(self, vuln_query_keys):
        self.vuln_query_keys = vuln_query_keys

    def evaluate(self, url):
        parsed_url = urlparse(url)
        parsed_qsl = parse_qsl(parsed_url.query)
        for qkey, qval in parsed_qsl:
            if qkey in self.vuln_query_keys and qval.startswith("http"):
                return True
        return False


class PathValueHeuristic(Heuristic):

    def __init__(self, vuln_query_keys):
        self.vuln_query_keys = vuln_query_keys

    def evaluate(self, url):
        parsed_url = urlparse(url)
        parsed_qsl = parse_qsl(parsed_url.query)
        for _, qval in parsed_qsl:
            if (qval.startswith("%2f")
                or qval.startswith("%2F")
                or qval.startswith("/")):
                return True
        return False

class URLValueHeuristic(Heuristic):

    def __init__(self, vuln_query_keys):
        self.vuln_query_keys = vuln_query_keys

    def evaluate(self, url):
        parsed_url = urlparse(url)
        parsed_qsl = parse_qsl(parsed_url.query)
        for _, qval in parsed_qsl:
            if qval.startswith("http"):
                return True
        return False

