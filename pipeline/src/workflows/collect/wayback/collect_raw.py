import luigi 
from urllib.parse import quote
from pathlib import Path

from ...logging import get_logger
from ...utils import LoadCSV

from candidate_collector.wayback import WaybackCollector
from candidate_collector.builders import RegexQueryBuilder
from candidate_collector.builders import ExpandSymbolsPreprocessor

from endpoint_analyzer import EndpointExtractor
from endpoint_analyzer import Type

class CollectDomainRaw(luigi.Task):
    """
    Fetch candidate URLs from wayback machine based on the provided arguments.

    Output: CSV
    Header: urls
    """

    #======================================================================
    # Task related params
    #======================================================================
    domain = luigi.parameter.Parameter(
            description = "The domain to prepare candidates for."
    )
    batch_size = luigi.parameter.IntParameter(
            description = "Numbers of URLs to fetch in each request for wayback machine."
    )
    from_date = luigi.parameter.Parameter(
            description = "Filter results based on when candidates were crawled."
    )
    to_date = luigi.parameter.Parameter(
            description = "Filter results based on when candidates were crawled."
    )
    max_requests = luigi.parameter.IntParameter(
            description = "Limits the maximum number of requests made."
    )
    

    #======================================================================
    # LoadCSV params for query keys
    #======================================================================
    qkeys_row_offset = luigi.parameter.IntParameter(
            description = "Offset for csv file."
    )
    qkeys_row_count = luigi.parameter.IntParameter(
            description = "Number of rows to consider. Any negative value to read an unlimited number of rows."
    )
    qkeys_csv_file = luigi.parameter.PathParameter(
            description = "The path to the csv file to load."
    )

    #======================================================================
    # General params
    #======================================================================
    out_dir = luigi.parameter.PathParameter(
            description = "The path to the output directory."
    )

    def requires(self):
        dependencies = dict()
        dependencies["qkeys"] = LoadCSV(
                row_offset=self.qkeys_row_offset,
                row_count=self.qkeys_row_count,
                csv_file=self.qkeys_csv_file,
                out_dir=self.out_dir)
        return dependencies

    def output(self):
        path = self.out_dir
        path = path / f"candidates"
        path = path / f"wayback"
        path = path / f"raw"
        path.mkdir(parents=True, exist_ok=True)
        filename = f"raw_urls_{self.domain}"
        filename += f"_{self.from_date}-{self.to_date}_{self.batch_size}_{self.max_requests}"
        filename += f"_qkeys_{self.qkeys_row_offset}_{self.qkeys_row_count}_{Path(str(self.qkeys_csv_file)).stem}"
        filename += f".csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        
        # Load all query parameter keys of interest
        with self.input()["qkeys"].open("r") as qkeys_file:
            qkeys = qkeys_file.read().splitlines()[1:]

        with self.output().open("w") as out_file:
            out_file.write("#url\n")
            collected_urls = []

            # Instantiate the endpoint extractor to remove near duplicates along the way
            extractor = EndpointExtractor(self.domain)

            # Build a regular expression only matching 'relevant' candidates
            regex = self.build_regex(self.domain, [], qkeys)

            # Wrapper to fetch raw wayback data for a given regex and domain
            wayback = WaybackCollector(
                    self.domain,
                    regex,
                    from_=self.from_date,
                    to=self.to_date,
                    limit=self.batch_size)

            prev_endpoint_count = 0


            try:
                for _ in range(self.max_requests):
                    urls, _ = wayback.fetch()
                    get_logger(__name__).info(regex)
                    collected_urls.extend(urls)

                    if not urls:
                        break
                    
                    # Train the endpoint extractor with the fetched URLs
                    extractor.train_with(collected_urls)
                    endpoints = extractor.endpoints()
                    # If no new endpoints we are done
                    if prev_endpoint_count == len(endpoints):
                        break
                    else:
                        prev_endpoint_count = len(endpoints)

                    # Update the regex based on extracted enpoints
                    regex = self.build_regex(self.domain, endpoints, qkeys)

                    wayback = WaybackCollector(
                            self.domain, regex,
                            from_=self.from_date,
                            to=self.to_date,
                            limit=self.batch_size)
            except Exception as e:
                out_file.write(f"Something went wrong: {str(e)}")


            out_file.write("\n".join(collected_urls))

    def build_regex(self, domain, endpoints, qkeys):
            pre_proc = ExpandSymbolsPreprocessor()
            pre_proc.expand("ANY", ".*")
            for type_name,_ in Type.BASE_TYPES:
                pre_proc.expand(type_name, Type.regex_for(type_name))

            builder = RegexQueryBuilder(domain)
            builder.ignore_trailing_slash()
            builder.register_preprocessor(pre_proc)

            # Constrain the regex based on specified query keys
            for key in qkeys:
                builder.require_query_key(key)

            # Alternatively look for query value that looks like a path or URL
            builder.require_query_value("/ANY")
            builder.require_query_value("%2fANY")
            builder.require_query_value("%2FANY")
            builder.require_query_value("httpANY")

            # Exclude the path for endpoints we already detected
            for endpoint in endpoints:
                path = "/".join(segment.strip("'") for segment in endpoint.path_type_trace)
                if path:
                    builder.exclude_path(quote(path))
            regex = builder.build()
            return regex
