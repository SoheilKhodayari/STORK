from urllib.parse import parse_qsl, urlparse
from typing import List
from ._base import URLStrategy

class ParamPollutionId(URLStrategy):
    """
    Preserves all original query string key value pairs
    """

    def __init__(self, *, params, **kwargs):
        # Initialize parameter list
        self.params = params
        super().__init__()

    def _is_url(self, value):
        value = value.lower()
        return value.startswith("http")

    def _is_path(self, value):
        value = value.lower()
        return value.startswith("%2f") or value.startswith("/")

    def _is_relevant(self, key, value):
        return self._is_url(value) or self._is_path(value) or (key in self.params)


    def collect(self, url) -> List[str]:

        parsed_url = urlparse(url)

        # Filter by set list of candidate parameters
        parsed_qs = parse_qsl(parsed_url.query)
        candidate_params = [qp for (qp, qv) in parsed_qs if self._is_relevant(qp, qv)]

        # Prepare candidates
        candidates = []
        for param in candidate_params:
            candidate_url = f"{url}&{param}={URLStrategy.PAYLOAD_PLACEHOLDER}"
            self.logger.info(f"New candidate: {candidate_url}")
            candidates.append(candidate_url)

        return candidates
