from typing import List
from urllib.parse import parse_qsl, quote, quote_plus, urlencode, urlparse, urlunparse

from abc import ABC, abstractmethod

from ...logging import get_logger


class URLStrategy(ABC):

    PAYLOAD_PLACEHOLDER = "PAYL0AD_PLAC3H0LD3R"

    def __init__(self, **kwargs):
        self.logger = get_logger(__name__)

    def _detect_encoding(self, url):
        parsed_url = list(urlparse(url))
        query = parse_qsl(parsed_url[4])
        encode_query = urlencode(query, quote_via=quote_plus)
        parsed_url[4] = encode_query
        unparsed_url = urlunparse(parsed_url)
        encoding_fn = quote
        if unparsed_url == url:
            encoding_fn = quote_plus
        return encoding_fn

    @classmethod
    def load_payload(cls, url, payload):
        return url.replace(URLStrategy.PAYLOAD_PLACEHOLDER, payload)

    @abstractmethod
    def collect(self, url: str) -> List[str]:
        return []

    def get_name(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.get_name()
