import luigi

from collections import defaultdict

from ..utils import load_json
from ..utils import save_json_stream

from endpoint_analyzer import EndpointExtractor
from urllib.parse import urlparse


class CollectCandidates(luigi.Task):

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

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"candidates.json")

    def run(self):
        data = load_json(self.src_file_json)

        candidates_payload = defaultdict(list)
        candidates_url = defaultdict(list)
        for entry in data:
            payload_strat = entry["payload_strat"]
            candidate_url = entry["candidate_url"]
            if payload_strat not in candidates_payload[candidate_url]:
                candidates_payload[candidate_url].append(payload_strat)
        sorted_candidates = dict(sorted(candidates_payload.items(), key=lambda x:x[0]))

        result = defaultdict(lambda: defaultdict(list))
        pl_key = "payloads"
        ca_key = "candidates"
        ep_key = "endpoints"
        for url, payload_strats in sorted_candidates.items():
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            for payload_strat in payload_strats:
                if payload_strat not in result[domain][pl_key]:
                    result[domain][pl_key].append(payload_strat)
            if url not in result[domain][ca_key]:
                result[domain][ca_key].append(url)

        for domain, entry in result.items():
            extractor = EndpointExtractor(domain)
            extractor.train_with(entry[ca_key])
            result[domain][ep_key] = [str(ep) for ep in extractor.endpoints()]

        with self.output().open("w") as file:
            save_json_stream(file, result)
