import requests
from urllib.parse import quote, urlencode


class DorkCollector:
    def __init__( self, dork_query, api_key, se_id):
        self.dork_query = dork_query
        self.dork_url = "https://www.googleapis.com/customsearch/v1?"
        self.params = [
            ("key", api_key),
            ("cx", se_id),
            ("q", dork_query),
        ]

    @classmethod
    def extract_urls(cls, data):
        return [item["link"] for item in data.get("items", [])]

    def query(self):
        return self.dork_url + urlencode(self.params)

    def fetch(self):
        query = self.query()
        response = requests.get(query)
        response.raise_for_status()
        self.data = response.json()
        return self.data
