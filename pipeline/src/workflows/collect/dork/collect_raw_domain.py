import luigi
import time

from ...utils import load_list
from ...utils import save_json_stream

from candidate_collector.dork import DorkCollector
from candidate_collector.builders import DorkQueryBuilder

class CollectRawDomain(luigi.Task):
    """
    Collect candidate URLs from google custom search engine.
    """

    #======================================================================
    # Resources
    #======================================================================
    resources = {"server": 1}

    #======================================================================
    # Files and Directories
    #======================================================================
    out_file_json = luigi.parameter.PathParameter(
            description = "The output file containing the prepared URLs."
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


    def output(self):
        return luigi.LocalTarget(self.out_file_json)


    def run(self):
        
        time.sleep(self.delay)
        
        # Ignore the query builder as the simple approach down below works way better
        # ---------------------------------------------------------------------------
        # qkeys = load_list(self.src_qkey_list)
        # builder = DorkQueryBuilder(self.domain)
        # for key in qkeys:
        #     builder.require_query_key(key)
        # dork_query = builder.build()

        dork_query = f"site:{self.domain} inurl:%3a%2f%2f"

        dork = DorkCollector(dork_query, self.api_key, self.se_id)
        try:
            data = dork.fetch()
        except Exception as e:
            data = {"error": repr(e)}

        with self.output().open("w") as file:
            save_json_stream(file, data)
