from collections import defaultdict
from ._oracle import Oracle
from ._parameter import Parameter
from .logging import get_logger
from urllib.parse import urlparse
from ._endpoint import Endpoint
from .heuristics import BranchingHeuristic


class EndpointExtractor:
    """Predict and classify URLs based on (sub)domain and path."""

    def __init__(self, tld):
        self.logger = get_logger(__name__)
        self.tld = tld
        self._domain_oracle = Oracle([], ".", tld)
        self._register_domain_heuristics(self._domain_oracle)
        self._path_oracles = dict()
        self._endpoints = dict()
        self.related_urls = set()

    def _register_path_heuristics(self, oracle):
        oracle.register_heuristic(BranchingHeuristic(num_branches=5))

    def _register_domain_heuristics(self, oracle):
        self._domain_oracle.register_heuristic(BranchingHeuristic(num_branches=3))

    def _path_oracle_for(self, type_trace):
        """Returns the oracle for a give type_trace or creates a new one."""
        if type_trace not in self._path_oracles:
            oracle = Oracle([], "/", "/")
            self._path_oracles[type_trace] = oracle
            self._register_path_heuristics(oracle)
        return self._path_oracles.get(type_trace)

    def train_with(self, urls):
        """Create type trees and models for provided urls to train endpoint extractor."""

        # Update list of related urls
        new_related_urls = self._filter_unrelated_urls(urls)
        self.related_urls = self.related_urls.union(new_related_urls)

        # Extract domain and path value traces
        path_value_traces = dict()
        domain_value_traces = dict()
        for url in self.related_urls:
            path_value_traces[url] = self._extract_path_value_trace(url)
            domain_value_traces[url] = self._extract_domain_value_trace(url)

        # Update domain oracle based on domain traces
        self._domain_oracle.update(domain_value_traces.values())
        domain_predictions_for_trace = self._domain_oracle.predict(
            domain_value_traces.values()
        )

        # Map URLs to domain type predictions
        domain_prediction_for_url = dict()
        for url in self.related_urls:
            domain_value_trace = domain_value_traces[url]
            domain_prediction_for_url[url] = domain_predictions_for_trace[
                domain_value_trace
            ]

        # Group path value traces based on domain predictions
        domain_groups = defaultdict(set)
        for url in self.related_urls:
            domain_predictions = domain_prediction_for_url[url]
            # Select the least abstract prediction
            domain_prediction = domain_predictions[0]
            path_value_trace = path_value_traces[url]
            domain_groups[domain_prediction].add(path_value_trace)

        # For each domain group update the corresponding path oracle
        # Populate endpoints for each domain type with all path type prediction
        for domain_prediction, path_value_traces in domain_groups.items():
            path_oracle = self._path_oracle_for(domain_prediction)
            path_oracle.update(path_value_traces)
            path_predictions = path_oracle.type_traces()
            for path_prediction in path_predictions:
                endpoint_key = (domain_prediction, path_prediction)
                self._endpoints[endpoint_key] = Endpoint(
                    domain_prediction, path_prediction
                )
        # Set parameters for endpoints
        self.logger.info(" # Set parameters for endpoints")
        for url in self.related_urls:
            endpoint = self.endpoints_for([url])[url]
            for parameter in Parameter.from_url(url):
                endpoint.add_parameter(parameter)

    def endpoints_for(self, urls):
        """Maps each url to an endpoint or None if the URL does not any endpoint."""
        endpoints = dict()
        for url in urls:
            domain_value_trace = self._extract_domain_value_trace(url)
            path_value_trace = self._extract_path_value_trace(url)
            domain_predictions = self._domain_oracle.predict([domain_value_trace])[domain_value_trace]
            if not domain_predictions:
                continue
            domain_prediction = domain_predictions[0]
            path_oracle = self._path_oracle_for(domain_prediction)
            path_predictions = path_oracle.predict([path_value_trace])[path_value_trace]
            if not path_predictions:
                continue
            path_prediction = path_predictions[0]
            endpoint_key = (domain_prediction, path_prediction)
            endpoint = self._endpoints.get(endpoint_key, None)
            endpoints[url] = endpoint
        return endpoints

    def endpoints(self):
        """List of all endpoints found so far"""
        return list(self._endpoints.values())

    def _filter_unrelated_urls(self, urls):
        """Returns a set of URLS matching the top level domain."""
        related_domains = set()
        unrelated_domain_count = 0
        for url in urls:
            netloc = urlparse(url).netloc
            if netloc.endswith(self.tld):
                related_domains.add(url)
            else:
                unrelated_domain_count += 1
        if unrelated_domain_count:
            self.logger.warn(
                f"Ignoring {unrelated_domain_count} unrelated URL not matching tld ({self.tld})"
            )
        return related_domains

    def _extract_domain_value_trace(self, url):
        netloc = urlparse(url).netloc
        domain_traces = netloc.split(".")
        return tuple(domain_traces)

    def _extract_path_value_trace(self, url):
        path = urlparse(url).path
        path_traces = path.split("/")[1:]
        return tuple(path_traces)
