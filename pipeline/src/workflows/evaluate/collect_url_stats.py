import luigi
import json

from ..utils import load_list
from ..utils import save_json_stream

from endpoint_analyzer import EndpointExtractor
from collections import defaultdict


class CollectUrlStats(luigi.Task):

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
        return luigi.LocalTarget(self.out_dir/f"url_stats.json")

    def run(self):
        result = defaultdict(dict)
        files = sorted(self.src_dir.glob("**/url*.csv"))
        for file in files:
            domain = file.stem.split("_")[1]
            urls = load_list(file)
            extractor = EndpointExtractor(domain)
            extractor.train_with(urls)
            endpoints = extractor.endpoints()
            result[domain]["urls"] = urls
            result[domain]["endpoints"] = [str(ep) for ep in endpoints]

        with self.output().open("w") as file:
            save_json_stream(file, result)
