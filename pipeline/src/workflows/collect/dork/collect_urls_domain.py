import luigi

from .collect_raw_domain import CollectRawDomain
from ...utils import load_json
from ...utils import save_list_stream

from candidate_collector.dork import DorkCollector

class CollectURLsDomain(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    out_dir = luigi.parameter.PathParameter(
            description = "The output dir containing the prepared URLs."
    )
    src_qkey_list = luigi.parameter.PathParameter(
            description = "The path to the file containing the URLs."
    )

    #======================================================================
    # Other
    #======================================================================
    domain = luigi.parameter.Parameter(
            description = "The domain to find candidates for."
    )

    se_id = luigi.parameter.Parameter(
            description = "Custom search engine id.",
            significant = False
    )

    api_key = luigi.parameter.Parameter(
            description = "Custom search engine api key.",
            significant = False
    )
    delay = luigi.parameter.IntParameter(
            description = "The delay to add after each task.",
            significant = False
    )

    def requires(self):
        dependencies = {}
        dependencies["raw"] = CollectRawDomain(
            out_file_json=self.out_dir/"data"/f"raw_{self.domain}.json",
            src_qkey_list=self.src_qkey_list,
            domain=self.domain,
            se_id=self.se_id,
            api_key=self.api_key,
            delay=self.delay)
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"urls_{self.domain}.csv")

    def run(self):
        dork_response = load_json(self.input()["raw"].path)
        urls = []
        if "error" not in dork_response:
            urls = DorkCollector.extract_urls(dork_response)

        with self.output().open("w") as file:
            save_list_stream(file, urls)
