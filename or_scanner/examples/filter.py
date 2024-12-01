from pprint import pprint
from or_scanner.strats.filter import EndpointFilter
from or_scanner.strats.filter import QueryKeyHeuristic, PathValueHeuristic, URLValueHeuristic 

def load_params():
    with open("data/parameters.csv") as param_file:
        params = param_file.read().splitlines()
    return params

def load_urls():
    with open("data/urls_9gag.com.csv") as url_file:
        urls = url_file.read().splitlines()
    return urls

def create_filter(domain, params):
    filter = EndpointFilter(domain)
    filter.register(QueryKeyHeuristic(params)) 
    filter.register(PathValueHeuristic(params)) 
    filter.register(URLValueHeuristic(params)) 
    return filter
    
    
def main():
    domain = "9gag.com"
    params = load_params()
    urls = load_urls()
    filter = create_filter(domain, params)
    filtered_urls = filter.filter(urls)
    pprint(filtered_urls)


if __name__ == "__main__":
    main()
