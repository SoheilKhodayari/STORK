from pprint import pprint
from or_scanner import CandidateBuilder
from or_scanner.strats.payload import IdentityPayload
from or_scanner.strats.url import QKeySingle, QKeyId, PathId, PathSingle, URLId, URLSingle, ParamPollutionId
from or_scanner.strats.filter import EndpointFilter
from or_scanner.strats.filter import QueryKeyHeuristic, PathValueHeuristic, URLValueHeuristic 

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
    # url_strat = QKeyId(params)
    # url_strat = QKeySingle(params)
    # url_strat = PathId()
    # url_strat = PathSingle()
    # url_strat = URLId()
    # url_strat = URLSingle()
    url_strat = ParamPollutionId(params=params)
    (builder
        .register(url_strat, IdentityPayload())
    )
    return builder

def get_candidates():
    domain = "vuln.test"
    params = load_params()
    urls = load_urls()
    filter = create_filter(domain, params)
    filtered_urls = filter.filter(urls)
    return filtered_urls
    
    
def main():
    verification_url = "https://verification-backend.test/"
    domain = "vuln.test"

    params = load_params()
    urls = load_urls()

    filter = create_filter(domain, params)
    filtered_urls = list(zip(*filter.filter(urls)))[1]

    builder = create_builder(verification_url, params)

    candidates = builder.build(filtered_urls, "manual")
    print(f"Number of candidates: {len(candidates)}")
    pprint(candidates)


if __name__ == "__main__":
    main()
