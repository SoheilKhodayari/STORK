import luigi 

from pathlib import Path

from .prepare_file_url_strat import PrepareFileURLStrat

from ..utils import load_json
from ..utils import save_json_stream
from ..utils import deserialize

class PrepareDirURLStrat(luigi.Task):

    """
    Prepares the URLs in a give csv file for the specified url strat.
    """

    #======================================================================
    # Files and Directories
    #======================================================================
    src_dir = luigi.parameter.PathParameter(
            description = "The path to the file containing the URLs."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory."
    )

    #======================================================================
    # Serialized params
    #======================================================================
    url_params_dict = luigi.parameter.Parameter(
            description = "Serialized parameters for the URL strategy."
    )

    #======================================================================
    # Other
    #======================================================================
    url_strat = luigi.parameter.Parameter(
            description = "The URL strategy to use."
    )

    def output(self):
        return luigi.LocalTarget(self.out_dir/"summary.json")

    def run(self):

        tasks = []
        for file in self.src_dir.glob("*.csv"):
            out_file = self.out_dir/"data"/f"{file.stem}.json"
            task = PrepareFileURLStrat(
                src_urls_list=file,
                url_params_dict=self.url_params_dict,
                out_file_json=out_file,
                url_strat=self.url_strat)
            tasks.append(task)
        yield tasks

        data = {}
        data["url_strat"] = self.url_strat
        data["strat_params"] = deserialize(self.url_params_dict)
        data["summary"] = []
        data["total_num_candidates"] = 0
        data["total_num_source_urls"] = 0
        data["domains"] = {}
        for task in tasks:
            entry = {}
            path = task.output().path
            prepared_urls = load_json(task.output().path)
            entry["domain"] = Path(path).stem.split("_")[1]
            entry["num_source_urls"] = prepared_urls["num_source_urls"]
            entry["endpoints"] = prepared_urls["endpoints"]
            entry["num_endpoints"] = prepared_urls["num_endpoints"]
            entry["num_contributed_urls"] = prepared_urls["num_contributed_urls"]
            data["summary"].append(entry)
            data["total_num_candidates"] += entry["num_endpoints"]
            data["total_num_source_urls"] += entry["num_source_urls"]
            if entry["num_endpoints"] > 0:
                data["domains"][entry["domain"]] = entry["num_endpoints"]
        data["total_num_domains"] = len(data["domains"])
        
        with self.output().open("w") as file:
            save_json_stream(file, data)
