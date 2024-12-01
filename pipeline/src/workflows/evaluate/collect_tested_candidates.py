import luigi

from urllib.parse import urlparse

from ..utils import load_json
from ..utils import save_json_stream

from collections import defaultdict
from endpoint_analyzer import EndpointExtractor


class CollectTestedCandidates(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_dir = luigi.parameter.PathParameter(
            description = "The path to the dir containing the evaluation logs."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory for everything manual analysis."
    )

    #======================================================================
    # Other
    #======================================================================

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"tested_candidates.json")


    def run(self):
        entries = defaultdict(lambda: defaultdict(list))
        results = self.src_dir.glob("**/results.json")

        ca_key = "candidates"
        ep_key = "endpoints"

        for file in results:
            data = load_json(file)
            for entry in data:
                url = entry["candidate_url"]
                domain = urlparse(url).netloc
                if url not in entries[domain]:
                    entries[domain][ca_key].append(url)

        for domain, entry in entries.items():
            extractor = EndpointExtractor(domain)
            extractor.train_with(entry[ca_key])
            endpoints = [str(ep) for ep in extractor.endpoints()]
            entries[domain][ep_key] = endpoints

        with self.output().open("w") as file:
            save_json_stream(file, entries)
