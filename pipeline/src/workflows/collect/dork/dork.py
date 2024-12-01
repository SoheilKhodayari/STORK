import random
import json
import luigi 
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from ..logging import get_logger

from .config import PipelineConfig
from .load_qkeys import LoadQueryKeys
from .load_domains import LoadDomains

from ..collector.dork import DorkCollector
from ..collector.builders import DorkQueryBuilder

from ..analyzer import EndpointExtractor



class CollectDorkDomainPrepareSimple(luigi.Task):
    domain_id = luigi.parameter.IntParameter()

    def requires(self):
        dependencies = {}
        dependencies["domains"] = LoadDomains()
        dependencies["qkeys"] = LoadQueryKeys()
        dependencies["endpoints"] = CollectDorkDomainEndpoints(domain_id=self.domain_id)
        dependencies["urls"] = CollectDorkDomainUrls(domain_id=self.domain_id)
        return dependencies

    def output(self):
        path = Path(f"outputs/luigi/dork/prepared/")
        path.mkdir(parents=True, exist_ok=True)
        filename = f"prepared_{self.domain_id}.csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        with self.input()["urls"].open("r") as url_file:
            urls  = url_file.read().splitlines()
        with self.input()["endpoints"].open("r") as endpoint_file:
            endpoints = endpoint_file.read().splitlines()
        with self.input()["domains"].open("r") as domain_file:
            domain = domain_file.read().splitlines()[self.domain_id]
        with self.input()["qkeys"].open("r") as qkey_file:
            qkeys = qkey_file.read().splitlines()


        with self.output().open("w") as out_file:
            extractor = EndpointExtractor(domain)
            extractor.train_with(urls)
            endpoints = extractor.endpoints()
            ep_for_url = extractor.endpoints_for(urls)
            prepared_urls = []
            for endpoint in endpoints:
                urls_for_ep = [url for url, ep in ep_for_url.items() if endpoint == ep]
                get_logger().info(f"Found {len(urls_for_ep)} URLs for endpoint {endpoint}")
                url = random.choice(urls_for_ep)
                prepared_urls.append(url)
            for url in prepared_urls:
                out_file.write(f"{url}\n")


class CollectDorkDomainEndpoints(luigi.Task):

    domain_id = luigi.parameter.IntParameter()

    def requires(self):
        dependencies = {}
        dependencies["urls"] = CollectDorkDomainUrls(domain_id=self.domain_id)
        dependencies["domains"] = LoadDomains()
        return dependencies

    def output(self):
        path = Path(f"outputs/luigi/dork/endpoints/")
        path.mkdir(parents=True, exist_ok=True)
        filename = f"endpoints_{self.domain_id}.csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        with self.input()["urls"].open("r") as url_file:
            urls  = url_file.read().splitlines()
        with self.input()["domains"].open("r") as domain_file:
            domain = domain_file.read().splitlines()[self.domain_id]

        with self.output().open("w") as out_file:
            extractor = EndpointExtractor(domain)
            extractor.train_with(urls)
            endpoints = extractor.endpoints()
            for endpoint in endpoints:
                out_file.write(f"{endpoint}\n")


class CollectDorkDomainUrls(luigi.Task):

    domain = luigi.parameter.Parameter(
            description = "The domain to prepare candidates for."
    )

    se_id = luigi.parameter.Parameter(
            description = "Custom search engine id.",
            significant = False
    )

    api_key = luigi.parameter.Parameter(
            description = "Custom search engine api key.",
            significant = False
    )

    def requires(self):
        dependencies = {}
        dependencies["urls"] = CollectDorkDomainRaw(
                domain_id=self.domain_id,
                se_id=self.se_id,
                api_key=self.api_key)
        return dependencies

    def output(self):
        path = Path(f"outputs/luigi/dork/urls/")
        path.mkdir(parents=True, exist_ok=True)
        filename = f"urls_{self.domain}.csv"
        return luigi.LocalTarget(path/filename)

    def run(self):
        with self.input()["urls"].open("r") as url_file:
            urls_raw = url_file.read()
            urls = []
            if not "Something went wrong:" in urls_raw:
                urls = DorkCollector.extract_urls(json.loads(urls_raw))

        with self.output().open("w") as out_file:
            for url in urls:
                out_file.write(f"{url}\n")



class CollectDorkDomainRaw(luigi.Task):

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


    def requires(self):
        dependencies = dict()
        dependencies["qkeys"] = LoadQueryKeys()
        return dependencies

    def output(self):
        path = Path(f"outputs/luigi/dork/raw")
        path.mkdir(parents=True, exist_ok=True)
        filename = f"raw_{self.domain}.csv"
        return luigi.LocalTarget(path/filename)


    def run(self):
        with self.input()["qkeys"].open("r") as qkeys_file:
            qkeys = qkeys_file.read().splitlines()
            qkeys = [qkey for qkey in qkeys if qkey[0].isalnum()]

        se_id = self.dork_se_id
        api_key = self.dork_api_key

        with self.output().open("w") as out_file:

            dork_query = self.build_dork_query(self.domain, qkeys)

            dork = DorkCollector(dork_query, api_key, se_id)
            try:
                get_logger(__name__).info(dork_query)
                data = dork.fetch()
                json.dump(data, out_file, indent=4)

            except Exception as e:
                out_file.write(f"Something went wrong: {str(e)}")


    def build_dork_query(self, domain, qkeys):
        builder = DorkQueryBuilder(domain)
        for key in qkeys:
            builder.require_query_key(key)
        dork_query = builder.build()
        return dork_query

