
import os

import luigi

from dotenv import load_dotenv

from workflows.evaluate import CollectVulnerable
from workflows.evaluate import CollectCandidates
from workflows.evaluate import CollectTestedCandidates
from workflows.evaluate import CollectScreenshots
from workflows.evaluate import CollectDialog
from workflows.evaluate import PrepareTableUnique
from workflows.evaluate import PreparePayloadScreenshots
from workflows.evaluate import PrepareXssScreenshots

from workflows.logging import configure_logging



def collect_xss_screenshots_args():
    list = []

    args = {}
    args["src_file_json"] = "outputs/test_screenshots.json"
    args["out_dir"] = "outputs/test_screenshots"
    args["out_name"] = "test_screenshots.txt"
    list.append(args)

    return list


def run():

    configure_logging()
    load_dotenv()

    config_path = "configs/debug.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)

    for args in collect_xss_screenshots_args():
        tasks = [ CollectDialog(**args)]
        luigi.build(tasks, workers=1, local_scheduler=True)

if __name__ == "__main__":
    run()

