import luigi 
from pathlib import Path

from .collect_raw import CollectDomainRaw

class CollectDomainURLs(luigi.Task):
    """
    Extracts URLs collected by CollectDomainRaw for for further processing.

    Output: CSV
    Header: urls
    """

    #======================================================================
    # CollectWaybackDomainRaw params
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
        dependencies = {}
        dependencies["urls"] = CollectDomainRaw(
                domain=self.domain,
                batch_size=self.batch_size,
                from_date=self.from_date,
                to_date=self.to_date,
                max_requests=self.max_requests,
                qkeys_row_offset=self.qkeys_row_offset,
                qkeys_row_count=self.qkeys_row_count,
                qkeys_csv_file=self.qkeys_csv_file,
                out_dir=self.out_dir)
        return dependencies

    def output(self):
        path = self.out_dir
        path = path / "candidates"
        path = path / "wayback"
        path = path / f"urls"
        path.mkdir(parents=True, exist_ok=True)
        filename = f"urls_{self.domain}"
        filename += f"_{self.from_date}-{self.to_date}_{self.batch_size}_{self.max_requests}"
        filename += f"_qkeys_{self.qkeys_row_offset}_{self.qkeys_row_count}_{Path(str(self.qkeys_csv_file)).stem}"
        filename += f".csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        with self.input()["urls"].open("r") as url_file:
            urls_raw = url_file.read().splitlines()[1:]
            urls = []
            for url_raw in urls_raw:
                if not "Something went wrong:" in url_raw:
                    urls.append(url_raw)

        with self.output().open("w") as out_file:
            out_file.write("#url\n")
            for url in urls:
                out_file.write(f"{url}\n")
