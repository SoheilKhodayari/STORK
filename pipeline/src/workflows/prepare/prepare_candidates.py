import luigi 
import random

from pathlib import Path

from or_scanner.strats.payload import PayloadFactory
from or_scanner.strats.url import URLStrategy

from ..utils import deserialize
from ..utils import load_json
from ..utils import save_json_stream

class PrepareCandidates(luigi.Task):

    """
    Prepares candidates for the given payload strat and URLs.
    """

    #======================================================================
    # Files and Directories
    #======================================================================
    src_dir = luigi.parameter.PathParameter(
            description = "The path to the directory containing the prepared URLs."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output file containing the prepared URLs."
    )

    #======================================================================
    # Serialized params
    #======================================================================
    payload_params_dict = luigi.parameter.Parameter(
            description = "Serialized parameters for the payload strategy."
    )

    #======================================================================
    # Other
    #======================================================================
    num_endpoints = luigi.parameter.Parameter(
            description = "Limit for the number of endpoints per domain."
    )
    payload_strat = luigi.parameter.Parameter(
            description = "The payload strategy to use."
    )
    redirect_target = luigi.parameter.Parameter(
            description = "The URL specifying the redirect target to create the payload for."
    )

    def output(self):
        return luigi.LocalTarget(self.out_dir/"candidates.json")


    def run(self):

        params = deserialize(self.payload_params_dict)
        factory = PayloadFactory()

        candidates = []
        for file in self.src_dir.glob("data/*.json"):
            prepared_urls = load_json(file)
            candidate_urls = prepared_urls["candidates"]
            candidate_urls = random.choices(candidate_urls, k=min(self.num_endpoints, len(candidate_urls)))
            for entry in candidate_urls:
                if not entry.get("derived_urls"):
                    continue
                candidate = {}
                candidate["candidate_url"] = random.choice(entry["derived_urls"])
                candidate["source_url"] = random.choice(entry["source_urls"])

                params["candidate_url"] = candidate["candidate_url"]
                payload_strat = factory.create_by_name(self.payload_strat, True, **params)
                payload = payload_strat.generate(self.redirect_target)
                candidate["payload"] = payload

                candidate["url_strat"] = self.src_dir.name
                candidate["payload_strat"] = self.payload_strat
                candidates.append(candidate)

        data = {}
        data["placeholder"] = URLStrategy.PAYLOAD_PLACEHOLDER
        data["candidates"] = candidates

        with self.output().open("w") as file:
            save_json_stream(file, data)
