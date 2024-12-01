from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from typing import List
from ._qkey_id import QKeyId




class QKeySingle(QKeyId):
    """
    Removes all query parameters that are considered irrelevant with regard to the payload
    """

    def __init__(self, *, params, **kwargs):
        super().__init__(params=params, **kwargs)

    def collect(self, url: str) -> List[str]:
        parsed_url = urlparse(url)
        parsed_url_parts = list(parsed_url)

        # Filter by set list of candidate parameters
        parsed_qs = parse_qsl(parsed_url.query, keep_blank_values=True)
        candidate_params = [qp for (qp, _) in parsed_qs if qp in self.params]

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
        result = self._flatten(
            [
                super(QKeySingle, self).collect(candidate)
                for candidate in candidates
            ]
        )
        return result

    def _flatten(self, candidates):
        return [url for urls in candidates for url in urls]
