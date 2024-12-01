import os

import luigi

from dotenv import load_dotenv

from workflows.collect.dork import CollectAll
from workflows.logging import configure_logging


def task_args():
    args = {}
    args["out_dir"] = "outputs/candidates/dork/"
    args["src_domain_list"] = "data/domains/random.csv"
    args["src_qkey_list"] = "indicators/prepared_qkeys.csv"
    args["api_key"] = os.environ.get("GOOGLE_API_KEY")
    args["se_id"] = os.environ.get("GOOGLE_SE_ID")
    args["delay"] = 30
    return args


def run():

    configure_logging()
    load_dotenv()

    config_path = "configs/debug.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)
 
    tasks = [CollectAll(**task_args())]
    luigi.build(tasks, workers=1, local_scheduler=True)

if __name__ == "__main__":
    run()

