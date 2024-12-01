from random import shuffle
from pprint import pprint
from endpoint_analyzer import EndpointExtractor
from urllib.parse import quote


def hand_crafted():
    domain = "example.com"
    urls = []
    urls.extend(urls_endpoint1(domain))
    urls.extend(urls_endpoint2(domain))
    urls.extend(urls_endpoint3(domain))
    urls.extend(urls_endpoint4(domain))
    urls.extend(urls_endpoint5(domain))
    urls.extend(urls_endpoint6(domain))
    urls.extend(urls_endpoint7(domain))
    urls.extend(urls_endpoint8(domain))
    urls.extend(urls_endpoint9(domain))
    shuffle(urls)

    extractor = EndpointExtractor(domain)
    extractor.train_with(urls)
    pprint(extractor.endpoints())
    import pdb; pdb.set_trace()

    # for oracle in extractor._path_oracles.values():
    #     for type_tree in oracle.type_trees.values():
    #         print(type_tree)


def urls_endpoint1(domain):
    endpoint = "/account/login"
    prefix = f"https://{domain}{endpoint}?next=%252f%253Fnext%253Dfoo"
    return [prefix]


def urls_endpoint2(domain):
    destination = "https://some-other-site.test/some-path/foo_bar?foo=bar"
    endpoint = f"/account/register?url={quote(destination)}"
    prefix = f"https://{domain}{endpoint}"
    return [prefix]


def urls_endpoint3(domain):
    endpoint = "/users"
    prefix = f"http://{domain}{endpoint}"
    names = ["admin", "jane", "doe", "foo", "bar", "baz"]
    return [f"{prefix}/{name}" for name in names]


def urls_endpoint4(domain):
    endpoint = "/r"
    prefix = f"https://{domain}{endpoint}"
    names = ["some-title", "another_title", "foo"]
    numbers = list(range(100, 1000, 69))
    return [f"{prefix}/{name}{number}" for number in numbers for name in names]


def urls_endpoint5(domain):
    endpoint = "/primes"
    prefix = f"https://numbers.{domain}{endpoint}"
    numbers = list(range(100, 1000, 42))
    return [f"{prefix}/{number}" for number in numbers]


def urls_endpoint6(domain):
    prefix = f"https://{domain}"
    numbers1 = list(range(500, 510))
    numbers2 = list(range(100, 110))
    return [
        f"{prefix}/{number1}/videos/{number2}"
        for number1 in numbers1
        for number2 in numbers2
    ]


def urls_endpoint7(domain):
    prefix = f"https://{domain}"
    names = [
        "bad",
        "verybad",
        "veryverybad",
        "notgood",
        "verynotgood",
        "veryverynotgood",
    ]
    return [f"{prefix}/{name}" for name in names]


def urls_endpoint8(domain):
    numbers1 = list(range(500, 510))
    numbers2 = list(range(100, 110))
    return [
        f"https://{abs(hash((number1, number2)))}.{domain}/{number1}/videos/{number2}"
        for number1 in numbers1
        for number2 in numbers2
    ]


def urls_endpoint9(domain):
    prefix = f"https://{domain}"
    numbers1 = list(range(550, 560))
    numbers2 = list(range(100, 110))
    return [
        f"{prefix}/{number1}/{number2}/{number1}"
        for number1 in numbers1
        for number2 in numbers2
    ]


def real_world(filename):
    with open(filename, "r") as f:
        urls = f.read().splitlines()

        extractor = EndpointExtractor("youtube.com")
        extractor.train_with(urls)
        # for oracle in extractor._path_oracles.values():
        #     for type_tree in oracle.type_trees.values():
        #         print(type_tree)
        pprint(extractor.endpoints())
        pprint(len(extractor.endpoints()))
        import pdb;pdb.set_trace()


if __name__ == "__main__":
    # hand_crafted()
    real_world("data/youtube.csv")
