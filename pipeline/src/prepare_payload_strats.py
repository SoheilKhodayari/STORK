import luigi

from pathlib import Path

from workflows.prepare import PrepareCandidates
from workflows.utils import serialize
from workflows.logging import configure_logging

from or_scanner.strats.payload import PayloadFactory


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
#===============================================================================

def task_args(url_strat, payload_strat):
    args = {}
    args["src_dir"] = Path(SRC_DIR)/url_strat
    args["out_dir"] = Path(OUT_DIR)/url_strat/payload_strat
    args["payload_params_dict"] = serialize(PARAMS)
    args["num_endpoints"] = 1
    args["payload_strat"] = payload_strat
    args["redirect_target"] = "https://verification-backend.test"
    return args

def run():

    configure_logging()

    # Read luigi config
    config_path = "configs/config.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)

    tasks = []
    for path in Path(SRC_DIR).glob("*/"):
        url_strat = path.name
        for payload_strat in STRATS:
            tasks.append(PrepareCandidates(**task_args(url_strat, payload_strat)))
    luigi.build(tasks, workers=1, local_scheduler=True)



if __name__ == "__main__":
    run()
