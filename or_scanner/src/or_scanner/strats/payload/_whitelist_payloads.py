from ._base import PayloadStrategy
from urllib.parse import urlparse, urlunparse

class PrependWhitelistPayload(PayloadStrategy):
    
    def __init__(self, add_tracking, *, candidate_url, **kwargs):
        super().__init__(add_tracking, **kwargs)
        self.candidate_url = candidate_url

    def generate(self, url):
        target_url = super().generate(url)
        parsed_url = urlparse(target_url)
        candidate_netloc  = urlparse(self.candidate_url).netloc
        old_netloc = parsed_url.netloc
        payload = urlunparse(parsed_url._replace(netloc=f"{candidate_netloc}.{old_netloc}"))
        return payload

class PrependAuthenticationPayload(PayloadStrategy):

    def __init__(self, add_tracking, *, candidate_url, **kwargs):
        super().__init__(add_tracking, **kwargs)
        self.candidate_url = candidate_url

    def generate(self, url):
        target_url = super().generate(url)
        parsed_url = urlparse(target_url)
        candidate_netloc = urlparse(self.candidate_url).netloc
        auth_pos = target_url.find(parsed_url.netloc)
        payload = f"{target_url[:auth_pos]}{candidate_netloc}@{target_url[auth_pos:]}"
        return payload

class DirectoryPayload(PayloadStrategy):

    def __init__(self, add_tracking, *, candidate_url, **kwargs):
        super().__init__(add_tracking, **kwargs)
        self.candidate_url = candidate_url

    def generate(self, url):
        target_url = super().generate(url)
        parsed_url = urlparse(target_url)
        candidate_netloc = urlparse(self.candidate_url).netloc
        payload = urlunparse(parsed_url._replace(path=f"https://{candidate_netloc}"))
        return payload
