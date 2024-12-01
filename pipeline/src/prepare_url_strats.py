import luigi

from workflows.utils import serialize
from workflows.utils import load_list
from workflows.logging import configure_logging
from workflows.prepare import PrepareDirURLStrat

from pathlib import Path

from or_scanner.strats.url import URLFactory

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
        

def task_args(url_strat):
    args = {}
# Path to src directory containing URL files for every domain to test
    args["src_dir"] = SRC_DIR
    args["out_dir"] = Path(OUT_DIR)/url_strat
    args["url_params_dict"] = serialize(PARAMS)
    args["url_strat"] = url_strat
    return args

def run():

    configure_logging()

    # Read luigi config
    config_path = "configs/config.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)

    tasks = []
    for url_strat in URL_STRATS:
        tasks.append(PrepareDirURLStrat(**task_args(url_strat)))
    luigi.build(tasks, workers=1, local_scheduler=True)



if __name__ == "__main__":
    run()
