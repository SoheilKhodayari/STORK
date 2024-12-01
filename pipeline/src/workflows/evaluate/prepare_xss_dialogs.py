
from collections import defaultdict
import random
import luigi
import uuid

from urllib.parse import urlparse

from ..utils import load_json
from ..utils import save_json_stream


class PrepareXssDialogs(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_file_json = luigi.parameter.PathParameter(
            description = "The path to the file with vulnerable entries."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory for everything manual analysis."
    )

    #======================================================================
    # Other
    #======================================================================
    payload = luigi.parameter.Parameter(
            description = "The payload to check for XSS."
    )
    name = luigi.parameter.Parameter(
            description = "The name of the XSS payload."
    )

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"xss_{self.name}.json")

    def run(self):
        data = load_json(self.src_file_json)

        urls = defaultdict(dict)
        placeholder = "PAYL0AD_PLAC3H0LD3R"
        domain_placeholder = "D0M4IN_PL4C3H0LD3R"

        payload_key = "payload"
        url_key = "url"
        domain_key = "domain"
        for domain, entry in data.items():
            name = str(uuid.uuid4())
            url = random.choice(entry["candidates"])
            netloc = urlparse(url).netloc
            url = url.replace(placeholder, self.payload)
            url = url.replace(domain_placeholder, netloc)
            urls[name][domain_key] = domain
            urls[name][url_key] = url
            modified_payload = self.payload.replace(domain_placeholder, netloc)
            urls[name][payload_key] = modified_payload



        with self.output().open("w") as file:
            save_json_stream(file, urls)

