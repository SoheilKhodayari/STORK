import random
import luigi
import time
import uuid

from collections import defaultdict

from or_scanner.strats.payload import PayloadFactory

from ..utils import load_json
from ..utils import save_json_stream

from playwright.sync_api import sync_playwright


class PreparePayloadScreenshots(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_file_json = luigi.parameter.PathParameter(
            description = "The path to the file with vulnerable entries."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory for everything manual analysis."
    )

    #======================================================================
    # Other
    #======================================================================
    target_url = luigi.parameter.Parameter(
            description = "The output directory for everything manual analysis."
    )

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"screenshots.json")

    def run(self):
        data = load_json(self.src_file_json)

        urls = defaultdict(dict)
        placeholder = "PAYL0AD_PLAC3H0LD3R"
        payload_factory = PayloadFactory()
        payload_params = { 
                "new_scheme": "//",
                "candidate_url": f"https://google.com"
                }

        payload_key  = "payload"
        url_key = "url"
        domain_key = "domain"
        for domain, entry in data.items():
            name = str(uuid.uuid4())
            payload_strat_name = random.choice(entry["payloads"])
            payload_strat = payload_factory.create_by_name(payload_strat_name, **payload_params)
            payload = payload_strat.generate(self.target_url)
            url = random.choice(entry["candidates"])
            url = url.replace(placeholder, payload)
            urls[name][domain_key] = domain
            urls[name][url_key] = url
            urls[name][payload_key] = payload

        # with sync_playwright() as p:

        #     browser = p.chromium.launch(channel="chrome")

        #     for domain, url in urls.items():
        #         page = browser.new_page()
        #         page.set_default_timeout(3000)
        #         page.goto(url)
        #         page.screenshot(path=f"{self.out_dir}/screenshots/img_{domain}.png", full_page=True)
        #         time.sleep(50000)

        with self.output().open("w") as file:
            save_json_stream(file, urls)

