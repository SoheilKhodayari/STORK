# STORK: Framework for Analysis of Open Redirects


### Installation Instructions

- `python -m venv venv`
- `source venv/bin/activate`
- `pip install requirements.txt`
- `pip install -e ../candidate_collector`
- `pip install -e ../endpoint_extractor`

Pipeline using the candidate_collector and endpoint_extractor package to fetch
and analyze data at scale. Uses luigi for pipeline scheduling and execution.

## Wayback Pipeline

To collect URLs from the Internet Archive you need to modify `src/wayback_collect_all.py` to point to
the correct config file by assigning the correct path to `config_path`. Sample config files can be found in `configs`.

Relevant section of config file:

```bash
[CollectAll]

# Specify how many URLs to fetch for a single request
batch_size=1000 

# Limit data range for when the URLs were crawled
from_date=202207
to_date=202301

# Limit the number of requests per domain
max_requests=5

# Specify the query keys that should be contained
qkeys_row_offset=0
qkeys_row_count=0
qkeys_csv_file=indicators/prepared_qkeys.csv

# Specify the domains to fetch URLs for
domains_row_offset=0
domains_row_count=0
domains_csv_file=/domains/tranco_top10k.csv

# Specify the output directory
out_dir=../../outputs/
```

#### How to Run:
```bash
cd src
python wayback_collect_all.py
```

## Dork Pipeline

To collect URLs from Google Programmable Search Engine you need to modify `src/dork_collect_all.py`.
(During development I overhauled the way agruments are provided to task, this is why this is different from `src/wayback_collect_all`.)


```python
def task_args():
    args = {}
    # The output directory
    args["out_dir"] = "outputs/candidates/dork/"
    # The path to the domain list to fetch URLs for
    args["src_domain_list"] = "data/domains/tranco_top10k.csv"
    # The path to the query key list to look for
    args["src_qkey_list"] = "indicators/prepared_qkeys.csv"
    # The environment variable storing the google api key
    args["api_key"] = os.environ.get("GOOGLE_API_KEY")
    # The environment variable storing the google se identifier
    args["se_id"] = os.environ.get("GOOGLE_SE_ID")
    # The delay after each subsequent requets to the google api.
    args["delay"] = 30
    return args
```

#### How to Run:
```bash
cd src
python dork_collect_all.py
```

## Prepare Abstract Candidates

To prepare the URLs in order to obtain a list of abstract candidates (URLs wich only lack the actual payload itself) run `src/prepare_url_strats.py`.
The following gives an overview of how to configure the script accordingly:


```python
#===============================================================================
# The URL strategies to prepare candidates for
URL_STRATS = URLFactory().list_strategies()

# The kwargs to pass to the constructor of each URL strat
PARAMS = {
    "params": load_list("indicators/prepared_qkeys.csv")
}

# Path to src directory containing URL files for every domain to test
SRC_DIR = "data/urls"

# Path to output directory for prepared URLS based on specified URL strats (STRATS)
OUT_DIR = f"outputs/url_strats"
#===============================================================================
```

#### How to Run:
```bash
cd src
python prepare_url_stats.py
```


## Prepare Candidates

To prepare the URLs in order to obtain a list of candidates for testing run `src/prepare_payload_strats.py`.
The following gives an overview of how to configure the script accordingly:


```python
#===============================================================================
# The payload strategies to prepare candidates for
STRATS = PayloadFactory().list_strategies()

# The kwargs to pass to the constructor of each payload strat
PARAMS = {
        "new_scheme": "//"
}

# Path to the output dir of 'prepare_url_strats' script
SRC_DIR = "outputs/url_strats"

# Path to output directory for final candidates ready to scan
OUT_DIR = f"outputs/prepared"

def task_args(url_strat, payload_strat):
    args = {}
    args["src_dir"] = Path(SRC_DIR)/url_strat
    args["out_dir"] = Path(OUT_DIR)/url_strat/payload_strat
    args["payload_params_dict"] = serialize(PARAMS)
    args["num_endpoints"] = 1
    args["payload_strat"] = payload_strat
    # The logging backend / backend used as oracle
    args["redirect_target"] = "https://verification-backend.test"
    return args

#===============================================================================
```

#### How to Run:
```bash
cd src
python prepare_payload_stats.py
```

## Test Candidates

To test the generated candidates in order to detect potential open redirects make sure that
the backend application runs at the specified domain. The following gives an overview of how to configure the script accordingly:
The number of workers correspond to the number of parallel browser instances opened. The batch size is the number of candidates per worker.


```python
#===============================================================================
# The secret used in the oracle
SECRET = "45fdbacd-8b08-4fa7-b801-7c1f84d7fe28"

# The number of candidates per batch
# IMPORTANT: If the batch size gets changed adjust the timeout in config!
BATCH_SIZE = 10

# The number of batches that are handled simultaniously
WORKERS = 1

# Path to the output dir of 'prepare_payload_strats'
SRC_DIR = "outputs/prepared"

# Path to output directory for prepared URLS based on specified URL strats (STRATS)
OUT_DIR = f"outputs/scan"
#===============================================================================
```

#### How to Run:
```bash
cd src
python scan_candidates.py
```

### Disclaimer

More than likely filepaths specified in scripts need to be adjusted according to your directory structure. It is probably the easiest to symlink the top level data directory of the repository to this folder.
