import luigi

from collections import defaultdict

from . import CollectVulnerable
from . import CollectCandidates
from . import CollectTestedCandidates

from ..utils import load_list
from ..utils import load_json
from ..utils import save_json_stream

from endpoint_analyzer import EndpointExtractor
from urllib.parse import urlparse


class PrepareTableUnique(luigi.Task):

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
        dependencies["vulnerable"] = CollectVulnerable(
                src_dir=self.src_dir,
                out_dir=self.out_dir)
        dependencies["candidates"] = CollectCandidates(
                src_file_json=self.out_dir/"vulnerable.json",
                out_dir=self.out_dir)
        dependencies["tested"] = CollectTestedCandidates(
                src_dir=self.src_dir,
                out_dir=self.out_dir)
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"unique_table_data.json")

    def run(self):

        result = defaultdict(dict)

        # Unique vulnerabilities
        data = load_json(self.input()["candidates"].path)
        unique_vuln_candidates = {domain: len(x["endpoints"]) for domain, x in data.items()}
        vuln_domains = list(unique_vuln_candidates.keys())

        # Unique URLs tested 
        data = load_json(self.input()["tested"].path)
        import pdb; pdb.set_trace()
        tested_candidates = {domain: len(x["endpoints"]) for domain, x in data.items() if domain in vuln_domains}

        # Non-unique URLs fetched
        files = list(self.src_dir.glob("**/collected/**/urls_*.csv"))
        urls = defaultdict(int)
        for file in files:
            name = file.stem
            domain = name.split("_")[1]
            for vuln_domain in vuln_domains:
                if domain in vuln_domain:
                    data = load_list(file)
                    urls[vuln_domain] += len(data)

        # Summarize
        ep_key = "unique_vulns"
        ca_key = "unique_urls"
        url_key = "urls"

        for domain in vuln_domains:
            result[domain][ep_key] = unique_vuln_candidates[domain]
            result[domain][ca_key] = tested_candidates[domain]
            result[domain][url_key] = urls[domain]


        with self.output().open("w") as file:
            save_json_stream(file, result)

