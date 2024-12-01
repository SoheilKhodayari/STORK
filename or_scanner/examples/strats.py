from pprint import pprint
from or_scanner.strats.payload import PayloadFactory
from or_scanner.strats.url import URLFactory


def load_params():
    with open("data/parameters.csv") as param_file:
        params = param_file.read().splitlines()
    return params

def load_urls():
    with open("data/urls_vuln.test.csv") as url_file:
        urls = url_file.read().splitlines()
    return urls

def payload_strats():
    factory = PayloadFactory()
    available_strats = factory.list_strategies()
    pprint(available_strats)

    url = "https://verification-backend.test"
    kwargs = {
            "new_scheme": "//",
            "candidate_url": "https://vuln.test?redir=foo"
    }

    pprint(f"Payloads for {url}:")
    payloads = []
    for strat_name in available_strats:
        strat = factory.create_by_name(strat_name, **kwargs)
        payload = strat.generate(url)
        payloads.append((strat_name, payload))
    pprint(payloads)



    pprint(f"Tracking payloads for {url}:")
    payloads = []
    for strat_name in available_strats:
        strat = factory.create_by_name(strat_name, True, **kwargs)
        try:
            payload = strat.generate(url)
            payloads.append((strat_name, payload))
        except Exception:
            pass
    pprint(payloads)

def url_strats():
    factory = URLFactory()
    available_strats = factory.list_strategies()
    pprint(available_strats)

    urls = load_urls()
    params = load_params()

    kwargs = {
            "params": params
    }

    pprint(f"---------------------------------------------")
    pprint(f"URLS")
    pprint(f"---------------------------------------------")
    pprint(urls)

    for strat_name in available_strats:
        pprint(f"---------------------------------------------")
        pprint(f"Strat: {strat_name}")
        pprint(f"---------------------------------------------")
        candidates = []
        for url in urls:
            strat = factory.create_by_name(strat_name, **kwargs)
            for candidate in strat.collect(url):
                candidates.append(candidate)
        pprint(candidates)
    

def main():
    url_strats()



if __name__ == "__main__":
    main()
