import luigi

from workflows.scan import ScanFile
from workflows.logging import configure_logging

from pathlib import Path


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

def task_args(url_strat, payload_strat):
    args = {}
    args["src_candidate_json"] = Path(SRC_DIR)/url_strat/payload_strat/"candidates.json"
    args["out_dir"] = Path(OUT_DIR)/url_strat/payload_strat
    args["backend_url"] = "https://verification-backend.test"
    args["secret"] = SECRET
    args["batch_size"] = BATCH_SIZE
    args["blacklist_list"] = Path("data") / "blacklist.csv"
    return args

def run():

    configure_logging()

    # Read luigi config
    config_path = "configs/config.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)

    tasks = []
    for url_path in Path(SRC_DIR).glob("*/"):
        url_strat = url_path.name
        for payload_path in url_path.glob("*/"):
            payload_strat = payload_path.name
            tasks.append(ScanFile(**task_args(url_strat, payload_strat)))
    luigi.build(tasks, workers=WORKERS, local_scheduler=True)


if __name__ == "__main__":
    run()
