import luigi 
import random

from ..utils import save_json_stream
from ..utils import deserialize
from ..utils import load_list

from or_scanner.drivers import PlaywrightDriver
from urllib.parse import urlparse

class ScanCandidates(luigi.Task):
    """
    Scans the provided list of candidates
    """

    #======================================================================
    # Files and Directories
    #======================================================================
    out_file_json = luigi.parameter.PathParameter(
            description = "The output file containing the result URLs."
    )
    blacklist_list = luigi.parameter.PathParameter(
            description = "Blacklisted domains that should not be testet."
    )
    #======================================================================
    # Serialized params
    #======================================================================
    candidate_dict = luigi.parameter.Parameter(
            description = "Serialized parameters for the URL strategy."
    )
    #======================================================================
    # Other
    #======================================================================
    secret = luigi.parameter.Parameter(
            description = "The oracle secret to look for."
    )
    backend_url = luigi.parameter.Parameter(
            description = "The URL of the backend target."
    )

    def output(self):
        return luigi.LocalTarget(self.out_file_json)

    def run(self):

        blacklist = load_list(self.blacklist_list)
        candidates = deserialize(self.candidate_dict)

        filtered_candidates = []
        for candidate in candidates:
            netloc = urlparse(candidate["candidate_url"]).netloc
            blacklisted = False
            for domain in blacklist:
                if domain in netloc:
                    blacklisted = True
            if not blacklisted:
                filtered_candidates.append(candidate)

        random.shuffle(filtered_candidates)
        
        
        driver = PlaywrightDriver(self.backend_url, filtered_candidates, self.secret)
        results = driver.execute()

        with self.output().open("w") as file:
            save_json_stream(file, results)
