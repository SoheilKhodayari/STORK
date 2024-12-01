import json
import time
from playwright.sync_api import sync_playwright
from ._base import BaseDriver
from ..strats.url import URLStrategy
from ..logging import configure_logging

class PlaywrightDriver(BaseDriver):

    def __init__(self, redirect_target, data, secret):
        super().__init__(redirect_target, data)
        self.secret = secret 
        configure_logging()


    def _visit(self):

        candidates = []
        fail_batch = False

        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome")

            for i, candidate in enumerate(self.data):

                self.logger.info(f"Progress: {i/len(self.data)}")

                if fail_batch:
                    raise Exception("Failing batch because of status code 429...")

                candidate_url = candidate["candidate_url"]
                payload = candidate["payload"]
                prepared_candidate_url = URLStrategy.load_payload(candidate_url, payload)

                page = browser.new_page(ignore_https_errors=True)
                page.set_default_timeout(BaseDriver.TIMEOUT_SECS*1000)

                start_time = time.time()

                try:
                    response = page.goto(prepared_candidate_url)
                    time.sleep(BaseDriver.TIMEOUT_SECS)
                    if response.ok:
                        if self._oracle(page, self.secret):
                            candidate["result"] = "vulnerable"
                            candidate["request"] = self._extract_request_data(page)
                            self.logger.info(f"Vulnerable: {prepared_candidate_url}") 
                        else:
                            candidate["result"] = "timeout"
                            self.logger.info(f"Timeout: {prepared_candidate_url}") 
                    else:
                        if response.status == "429":
                            fail_batch = True
                        error = f"{response.status}|{response.status_text}"
                        candidate["result"] = error
                        self.logger.info(f"{error}: {prepared_candidate_url}")
                except Exception as e:
                    error = repr(e)
                    candidate["result"] = f"crash({error})"
                    self.logger.error(f"Crash: {prepared_candidate_url}")
                    page.close()
                    browser.close()
                    browser = p.chromium.launch(channel="chrome")
                finally:
                    candidate["time"] = start_time
                    page.close()
                    candidates.append(candidate)

            browser.close()
        return candidates


    def _extract_request_data(self, page):
        fn = (
                f"() => {{\n"
                f"  var data = {{}}\n"
                f"  data['time'] = document.getElementById('time').textContent\n"
                f"  data['iframe'] = document.getElementById('iframe').textContent\n"
                f"  data['method'] = document.getElementById('method').textContent\n"
                f"  data['url'] = window.location.href\n"
                f"  data['fragment'] = window.location.hash\n"
                f"  data['args'] = document.getElementById('args').textContent\n"
                f"  data['form'] = document.getElementById('form').textContent\n"
                f"  data['json'] = document.getElementById('json').textContent\n"
                f"  data['cookies'] = JSON.parse(document.getElementById('cookies').textContent)\n"
                f"  data['headers'] = document.getElementById('headers').textContent\n"
                f"  return JSON.stringify(data)\n"
                f"}}"
            )
        data = json.loads(page.evaluate(fn))
        return data

    def _oracle(self, page, secret):
        fn = (
                f"() => {{\n"
                f"  element = document.getElementById('{secret}')\n"
                f"  return element != null;\n"
                f"}}"
            )
        result = page.evaluate(fn)
        return result
