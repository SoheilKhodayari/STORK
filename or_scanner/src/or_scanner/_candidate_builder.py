import os
from collections import defaultdict

from .logging import get_logger
import requests

class CandidateBuilder:
    
    BACKEND_SECRET = "45fdbacd-8b08-4fa7-b801-7c1f84d7fe28"
    BACKEND_ENV_KEY = "BACKEND_SECRET"

    def _get_expected_secret(self):
        return os.environ.get(CandidateBuilder.BACKEND_ENV_KEY, CandidateBuilder.BACKEND_SECRET)


    def __init__(self, backend_url):
        self.logger = get_logger(__name__)
        try:
            # Verify that the backend is reachable as integrity check
            requests.head(backend_url, verify=False)
        except Exception:
            error_msg = "Cannot reach backend. Aborting..."
            self.logger.error(error_msg)
            raise ValueError(error_msg)
        self.backend_url = backend_url.rstrip("/")
        self.strategies = []

    def register(self, url_strat, payload_strat):
        # Register a payload strategy for a given url strategy
        self.logger.info(
            f"Registered strategy: ({url_strat.get_name()}, {payload_strat.get_name()})"
        )
        self.strategies.append((url_strat, payload_strat))
        return self

    def build(self, urls, source):
        # Builds a set of candidates based on registered strategies

        collected_candidates = []

        # Creates candidate URLs based and registered strategies and maps URL
        # to set of strategies that created the URL
        candidate_strats_map, candidate_url_map = self._get_url_candidates(urls)

        # Create candidates based on registered strategies
        for candidate_url, url_strats in candidate_strats_map.items():
            url_strat_name = " ".join(str(strat) for strat in url_strats)

            # Retrieve registered payload strats for given url_strat
            payload_strats = self._get_payload_strats(url_strats)

            for payload_strat in payload_strats:
                secret = self._get_expected_secret()
                verification_url = self._create_verification_url(secret)
                payload = payload_strat.generate(verification_url)
                payload_strat_name = payload_strat.get_name()
                candidate = {}
                candidate["candidate_url"] = candidate_url
                candidate["secret"] = secret
                candidate["payload"] = payload
                candidate["derived_from"] = " ".join(candidate_url_map[candidate_url])
                candidate["url_strat_name"] = url_strat_name
                candidate["payload_strat_name"] = payload_strat_name
                candidate["obtained_from"] = source
                collected_candidates.append(candidate)
        return collected_candidates

    def _create_verification_url(self, secret):
        return f"{self.backend_url}"

    def _get_payload_strats(self, url_strats):
        # For a given url strategy return all payloads registered for that strategy
        payload_strats = [
            payload_strat
            for url_strat, payload_strat in self.strategies
            if url_strat in url_strats
        ]
        return payload_strats


    def _get_url_candidates(self, urls):
        # Creates a mapping of candidates to url strats that created them
        url_strats, _ = list(zip(*self.strategies))
        candidate_strats_map = defaultdict(set)
        candidate_url_map = defaultdict(set)
        for url in urls:
            for url_strat in url_strats:
                candidates = url_strat.collect(url)
                for candidate in candidates:
                    candidate_strats_map[candidate].add(url_strat)
                    candidate_url_map[candidate].add(url)
        return candidate_strats_map, candidate_url_map
