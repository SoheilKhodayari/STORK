import luigi

from .scan_candidates import ScanCandidates 

from ..utils import serialize
from ..utils import load_json
from ..utils import save_json_stream

class ScanFile(luigi.Task):

    """
    Scans the given candidate file.
    """

    #======================================================================
    # Files and Directories
    #======================================================================
    src_candidate_json = luigi.parameter.PathParameter(
            description = "The path to the file containing candidates."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output file containing the result URLs."
    )
    blacklist_list = luigi.parameter.PathParameter(
            description = "Blacklisted domains that should not be testet."
    )
    #======================================================================
    # Other
    #======================================================================
    backend_url = luigi.parameter.Parameter(
            description = "The URL of the backend target."
    )
    secret = luigi.parameter.Parameter(
            description = "The URL of the backend target."
    )
    batch_size = luigi.parameter.IntParameter(
            description = "Then number of candidates per batch."
    )

    def output(self):
        return luigi.LocalTarget(self.out_dir/"results.json")


    def run(self):
        candidates = load_json(self.src_candidate_json)["candidates"]
        num_batches = len(candidates) // self.batch_size
        if num_batches == 0:
            num_batches = 1

        tasks = []
        for i in range(num_batches):
            start = i * self.batch_size
            end = i * self.batch_size + self.batch_size
            task = ScanCandidates(
                    out_file_json=self.out_dir/"data"/f"candidates_{start}_{end}.json",
                    blacklist_list=self.blacklist_list,
                    candidate_dict=serialize(candidates[start:end]),
                    backend_url=self.backend_url,
                    secret=self.secret)
            tasks.append(task)
        yield tasks

        results = []
        for task in tasks:
            path = task.output().path
            for result in load_json(path):
                results.append(result)


        with self.output().open("w") as file:
            save_json_stream(file, results) 
