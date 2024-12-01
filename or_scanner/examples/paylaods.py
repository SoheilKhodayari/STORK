from pprint import pprint
from or_scanner.strats.payload import PayloadFactory
    

def main():

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


if __name__ == "__main__":
    main()
