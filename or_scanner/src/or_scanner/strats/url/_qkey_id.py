from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from typing import List
from ._base import URLStrategy

class QKeyId(URLStrategy):
    """
    Preserves all original query string key value pairs
    """

    def __init__(self, *, params, **kwargs):
        # Initialize parameter list
        self.params = params
        super().__init__()


    def collect(self, url) -> List[str]:

        parsed_url = urlparse(url)

        # Filter by set list of candidate parameters
        parsed_qs = parse_qsl(parsed_url.query, keep_blank_values=True)
        candidate_params = [qp for (qp, _) in parsed_qs if qp in self.params]

        # Prepare candidates
        candidates = []
        for param in candidate_params:
            parsed_url_parts = list(parsed_url)
            query = [
                (key, URLStrategy.PAYLOAD_PLACEHOLDER)
                if key == param
                else (key, value)
                for (key, value) in parsed_qs
            ]
            # Preserve original encoding
            encoded_query = urlencode(query, quote_via=self._detect_encoding(url))
            parsed_url_parts[4] = encoded_query
            candidate_url = urlunparse(parsed_url_parts)
            self.logger.info(f"New candidate: {candidate_url}")
            candidates.append(candidate_url)

        return candidates
