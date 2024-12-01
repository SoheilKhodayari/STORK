from ...logging import get_logger
from abc import ABC, abstractmethod
from urllib.parse import urlparse, parse_qsl

class URLFilter(ABC):
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.heuristics = []


    def register(self, heuristic):
        # Register a heuristic to contribute to the score
        self.logger.info(
            f"Registered strategy: ({heuristic.get_name()})"
        )
        self.heuristics.append(heuristic)
        return self

    def evaluate(self, url):
        # Assign score to a single URL based on registered heuristics
        score = 0
        for heuristic in self.heuristics:
            if heuristic.evaluate(url):
                score += 1
        return score / len(self.heuristics)

    def assign_score(self, urls):
        # Assign the URLs the corresponding scores and sort the result by
        # score. URLs with more query parameters are favoured.
        score_for_urls = [self.evaluate(url) for url in urls]
        url_scores = list(zip(score_for_urls, urls))
        url_scores.sort(key=lambda entry: len(parse_qsl(urlparse(entry[1]).query)), reverse=True)
        url_scores.sort(key=lambda entry: entry[0], reverse=True)
        return url_scores

    @abstractmethod
    def filter(self, urls, num_candidates):
        pass
