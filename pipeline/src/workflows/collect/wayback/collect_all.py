import luigi

from pathlib import Path

from .collect_urls import CollectDomainURLs
from ...utils import LoadCSV

class CollectAll(luigi.Task):
    """
    Creates a file containing candidate URLs for each domain specified for which
    there was data found using this approach. 

    Output: CSV
    Header: urls
    """

    #======================================================================
    # CollectWaybackDomainRaw params
    #======================================================================
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
    # LoadCSV for domains
    #======================================================================
    domains_row_offset = luigi.parameter.IntParameter(
            description = "Offset for csv file."
    )
    domains_row_count = luigi.parameter.IntParameter(
            description = "Number of rows to consider. Any negative value to read an unlimited number of rows."
    )
    domains_csv_file = luigi.parameter.PathParameter(
            description = "The path to the csv file to load."
    )

    #======================================================================
    # General params
    #======================================================================
    out_dir = luigi.parameter.PathParameter(
            description = "The path to the output directory."
    )

    def requires(self):
        dependencies = {}
        dependencies["domains"] = LoadCSV(
                row_offset=self.domains_row_offset,
                row_count=self.domains_row_count,
                csv_file=self.domains_csv_file,
                out_dir=self.out_dir)
        return dependencies

    def output(self):
        path = self.out_dir
        path = path / "candidates"
        path = path / "wayback"
        path = path / "summary"
        path.mkdir(parents=True, exist_ok=True)
        filename = f"summary"
        filename += f"_{self.from_date}-{self.to_date}_{self.batch_size}_{self.max_requests}"
        filename += f"_domains_{self.domains_row_offset}_{self.domains_row_count}_{Path(str(self.domains_csv_file)).stem}"
        filename += f"_qkeys_{self.qkeys_row_offset}_{self.qkeys_row_count}_{Path(str(self.qkeys_csv_file)).stem}"
        filename += f".csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        # Get all domains for which we want to collect data
        with self.input()["domains"].open("r") as domain_file:
            domains = domain_file.read().splitlines()[1:]

        # Candidates
        all_candidates = []

        # Prepare candidate URLs for each domain
        prepared = []
        for domain in domains:
            prepared.append(CollectDomainURLs(
                domain=domain,
                batch_size=self.batch_size,
                from_date=self.from_date,
                to_date=self.to_date,
                max_requests=self.max_requests,
                qkeys_row_offset=self.qkeys_row_offset,
                qkeys_row_count=self.qkeys_row_count,
                qkeys_csv_file=self.qkeys_csv_file,
                out_dir=self.out_dir
                ))
        yield prepared

        for i, task in enumerate(prepared):
            with task.output().open("r") as prepared_file:
                domain = domains[i]
                rows = prepared_file.read().splitlines()[1:]
                all_candidates.append((domain, len(rows)))
            
        with self.output().open("w") as out_file:
            out_file.write(f"#num_candidates;domain\n")
            for domain, num_candidates in all_candidates:
                out_file.write(f"{num_candidates};{domain}\n")
