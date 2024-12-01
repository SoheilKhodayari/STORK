

from collections import defaultdict
import random
import luigi
import uuid
import time


from or_scanner.strats.payload import PayloadFactory

from ..utils import load_json
from ..utils import load_list
from ..utils import save_json_stream

from playwright.sync_api import sync_playwright


class CollectScreenshots(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_file_json = luigi.parameter.PathParameter(
            description = "The path to the file with vulnerable entries."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory for everything manual analysis."
    )
    out_name = luigi.parameter.Parameter(
            description = "Then name for the file to signal screenshots were taken."
    )

    #======================================================================
    # Other
    #======================================================================

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/self.out_name)

    def run(self):
        data = load_json(self.src_file_json)


        with sync_playwright() as p:

            browser = p.chromium.launch(channel="chrome")

            for id, entry in data.items():
                url = entry["url"]
                domain = entry["domain"]
                page = browser.new_page(ignore_https_errors=True)
                page.set_default_timeout(3*1000)
                try:
                    page.goto(url)
                    page.screenshot(path=f"{self.out_dir}/screenshots/img_{domain}_{id}.png", full_page=True)
                except:
                    print(f"Unable to take screenshot for {url}")
                    continue
                finally:
                    time.sleep(300000)


        with self.output().open("w") as file:
            save_json_stream(file, {})

