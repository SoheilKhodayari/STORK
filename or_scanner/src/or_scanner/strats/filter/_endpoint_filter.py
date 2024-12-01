from endpoint_analyzer import EndpointExtractor
from ._base import URLFilter

class EndpointFilter(URLFilter):
    """
    Filters URLs based on endpoints and heuristics
    """

    def __init__(self, domain):
        super().__init__()
        self.domain = ".".join(domain.split(".")[-2:])

    def filter(self, urls, num_candidates=1):
        """
        Based on registered heuristics picks the URLS that are "most likely"
        to be vulnerable and picks num_candidate URLs per endpoint
        """

        filtered_urls = []

        extractor = EndpointExtractor(self.domain)
        extractor.train_with(urls)
        endpoints = extractor.endpoints()
        ep_for_url = extractor.endpoints_for(urls)

        for endpoint in endpoints:
            # Collect all URLs for a given endpoint
            urls_for_ep = [url for url, ep in ep_for_url.items() if endpoint == ep]
            url_scores = self.assign_score(urls_for_ep)
            best_urls = url_scores[:num_candidates]
            filtered_urls.extend(best_urls)

        filtered_urls.sort(key=lambda entry: entry[0], reverse=True)
        return filtered_urls

