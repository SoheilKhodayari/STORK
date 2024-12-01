from pprint import pprint
from or_scanner import CandidateBuilder
from or_scanner.strats.payload import IdentityPayload, PrependWhitelistPayload
from or_scanner.strats.url import PathId, QKeyId
from or_scanner.strats.filter import EndpointFilter
from or_scanner.strats.filter import QueryKeyHeuristic, PathValueHeuristic, URLValueHeuristic 
from or_scanner.drivers import PlaywrightDriver
from or_scanner.logging import configure_logging

def load_params():
    with open("data/parameters.csv") as param_file:
        params = param_file.read().splitlines()
    return params

def load_urls():
    with open("data/urls_vuln.test.csv") as url_file:
        urls = url_file.read().splitlines()
    return urls

def create_filter(domain, params):
    filter = EndpointFilter(domain)
    filter.register(QueryKeyHeuristic(params)) 
    filter.register(PathValueHeuristic(params)) 
    filter.register(URLValueHeuristic(params)) 
    return filter

def create_builder(verification_url, params):
    builder = CandidateBuilder(verification_url)
    id_url_strat = QKeyId(params)
    (builder
        .register(id_url_strat, PrependWhitelistPayload())
    )
    return builder

    
def main():
    configure_logging()

    verification_url = "https://verification-backend.test/"
    domain = "vuln.test"

    params = load_params()
    urls = load_urls()
    secret = "45fdbacd-8b08-4fa7-b801-7c1f84d7fe28"
    
    filter = create_filter(domain, params)
    filtered_urls = list(zip(*filter.filter(urls)))[1]

    builder = create_builder(verification_url, params)

    candidates = builder.build(filtered_urls, "manual")
    pprint(candidates)

    driver = PlaywrightDriver(verification_url, candidates, secret)
    vuln_candidates = driver.execute()
    print(f"Number of vulnerable candidates: {len(vuln_candidates)}")
    pprint(vuln_candidates)


if __name__ == "__main__":
    main()
