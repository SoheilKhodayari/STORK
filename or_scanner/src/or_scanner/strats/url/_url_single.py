from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from typing import List
from ._url_id import URLId

class URLSingle(URLId):
    """
    Removes all query parameters that are considered irrelevant with regard to the payload
    """

    def _is_url(self, value):
        value = value.lower()
        return value.startswith("http")

    def collect(self, url: str) -> List[str]:

        parsed_url = urlparse(url)
        parsed_url_parts = list(parsed_url)

        # Filter by set list of candidate parameters
        parsed_qs = parse_qsl(parsed_url.query)
        candidate_params = [qp for (qp, qv) in parsed_qs if self._is_url(qv)]

        # Prepare candidates
        candidates = []
        for key, value in parsed_qs:
            if key in candidate_params:
                encoded_query = urlencode(
                    [(key, value)], quote_via=self._detect_encoding(url)
                )
                parsed_url_parts[4] = encoded_query
                candidate_url = urlunparse(parsed_url_parts)
                candidates.append(candidate_url)
        return self._flatten(
            [
                super(URLSingle, self).collect(candidate)
                for candidate in candidates
            ]
        )

    def _flatten(self, candidates):
        return [url for urls in candidates for url in urls]
