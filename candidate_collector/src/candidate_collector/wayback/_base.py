import requests
from urllib.parse import quote, urlencode


class WaybackCollector:
    def __init__(
        self, domain, regex, *, limit=None, from_=None, to=None, resume_key=None
    ):
        self.domain = domain
        self.regex = regex
        self.wayback_url = f"https://web.archive.org/cdx/search/cdx?"
        self.params = [
            ("url", f"{self.domain}"),
            ("filter", f"original:{regex}"),
            ("showResumeKey", "true"),
            ("output", "json"),
            ("filter", "statuscode:200"),
            ("collapse", "urlkey"),
            ("fl", "original"),
            ("matchType", "domain"),
        ]
        if limit:
            self.params.append(("limit", limit))
        if from_:
            self.params.append(("from", from_))
        if to:
            self.params.append(("to", to))
        if resume_key:
            self.params.append(("resumeKey", resume_key))

    def query(self):
        return self.wayback_url + urlencode(self.params)

    def fetch(self):
        query = self.query()
        response = requests.get(query)
        response.raise_for_status()
        data = response.json()
        # First line is description of fields
        if len(data) > 0:
            data.pop(0)

        resume_key = None
        # Resume key is last line and preceded by an empty line
        if len(data) >= 2 and not data[-2]:
            resume_key = data.pop()[0]
            data.pop()

        urls = [url[0] for url in data]

        return urls, resume_key
