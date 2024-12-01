import luigi

from .collect_urls_domain import CollectURLsDomain
from ...utils import load_list
from ...utils import save_json_stream

class CollectAll(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    out_dir = luigi.parameter.PathParameter(
            description = "The output dir containing the prepared URLs."
    )
    src_domain_list = luigi.parameter.PathParameter(
            description = "The path to the file containing the URLs."
    )
    src_qkey_list = luigi.parameter.PathParameter(
            description = "The path to the file containing the URLs."
    )

    #======================================================================
    # Other
    #======================================================================
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
        domains = load_list(self.src_domain_list)

        dependencies = {}
        dependencies["urls"] = {}
        for domain in domains:
            task = CollectURLsDomain(
                out_dir=self.out_dir/"data",
                src_qkey_list=self.src_qkey_list,
                domain=domain,
                se_id=self.se_id,
                api_key=self.api_key,
                delay=self.delay)
            dependencies["urls"][domain] = task
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/"summary.json")

    def run(self):

        data = {}
        for domain, urls_target in self.input()["urls"].items():
            urls = load_list(urls_target.path)
            data[domain] = len(urls)

        with self.output().open("w") as file:
            save_json_stream(file, data)



