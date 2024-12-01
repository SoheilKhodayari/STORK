from collections import defaultdict
import luigi 

from ..utils import load_list
from ..utils import save_json_stream
from ..utils import deserialize

from endpoint_analyzer import EndpointExtractor
from or_scanner.strats.url import URLFactory

class PrepareFileURLStrat(luigi.Task):

    """
    Prepares the URLs for a given URL strat.
    """

    #======================================================================
    # Files and Directories
    #======================================================================
    src_urls_list = luigi.parameter.PathParameter(
            description = "The path to the file containing the URLs."
    )
    out_file_json = luigi.parameter.PathParameter(
            description = "The output file containing the prepared URLs."
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
        return luigi.LocalTarget(self.out_file_json)


    def run(self):

        # Initialize
        source_urls = load_list(self.src_urls_list)
        params = deserialize(self.url_params_dict)
        factory = URLFactory()
        url_strat = factory.create_by_name(self.url_strat, **params)
        domain = self.src_urls_list.stem.split("_")[1]

        # Extract candidates
        candidates = defaultdict(set)
        for source_url in source_urls:
            derived_urls = url_strat.collect(source_url)
            for url in derived_urls:
                candidates[url].add(source_url)

        # Keep track of urls that contributed to candidates
        contributed_urls = set()
        for url_set in candidates.values():
            for url in url_set:
                contributed_urls.add(url)
        contributed_urls = list(contributed_urls)

        # Extract endpoints of source urls
        extractor = EndpointExtractor(domain)
        extractor.train_with(contributed_urls)
        endpoints = extractor.endpoints()
        ep_for_url = extractor.endpoints_for(contributed_urls)

        source_urls_for_endpoint = defaultdict(set)
        derived_urls_for_endpoint = defaultdict(set)
        # Find one candidate for each endpoint
        for endpoint in endpoints:
            for derived_url, urls in candidates.items():
                for url in urls:
                    if url in ep_for_url and ep_for_url[url] == endpoint:
                        source_urls_for_endpoint[endpoint].add(url)
                        derived_urls_for_endpoint[endpoint].add(derived_url)

        data = {}
        data["num_source_urls"] = len(source_urls)
        data["endpoints"] = [str(endpoint) for endpoint in endpoints]
        data["num_endpoints"] = len(endpoints)
        data["num_contributed_urls"] = len(contributed_urls)
        data["candidates"] = []
        for endpoint in endpoints:
            entry = {}
            entry["endpoint"] = str(endpoint)
            entry["derived_urls"] = list(derived_urls_for_endpoint[endpoint])
            entry["source_urls"] = list(source_urls_for_endpoint[endpoint])
            data["candidates"].append(entry)

        with self.output().open("w") as file:
            save_json_stream(file, data)
