from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import time
import json
from ._base import BaseDriver
from ..strats.url import URLStrategy
from ..logging import configure_logging

from xvfbwrapper import Xvfb

class SeleniumDriver(BaseDriver):

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")

        driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager().install()),
                chrome_options=options) 

        driver.implicitly_wait(BaseDriver.TIMEOUT_SECS)
        driver.set_page_load_timeout(BaseDriver.TIMEOUT_SECS)
        driver.set_script_timeout(BaseDriver.TIMEOUT_SECS)
        return driver


    def _visit(self):

        configure_logging()

        with Xvfb() as _:
            candidates = []
            driver = self._init_driver()

            for i, candidate in enumerate(self.data):

                start_time = time.time()

                self.logger.info(f"Progress: {i/len(self.data)}")

                candidate_url = candidate["candidate_url"]
                payload = candidate["payload"]
                secret = self.secret
                prepared_candidate_url = URLStrategy.load_payload(candidate_url, payload)


                try:
                    driver.get(prepared_candidate_url)
                except TimeoutException as e:
                    candidate["result"] = "page-load-timeout"
                    self.logger.info(f"Page load timeout: {prepared_candidate_url}") 
                except Exception as e:
                    error = self._sanatize_str(repr(e))
                    candidate["result"] = f"crash({error})"
                    self.logger.error(f"Crash: {prepared_candidate_url}")
                    driver.close()
                    driver = self._init_driver()
                    end_time = time.time()
                    candidate["time"] = end_time - start_time
                    candidates.append(candidate)
                    continue

                time.sleep(BaseDriver.TIMEOUT_SECS)

                try:
                    if self._oracle(driver, secret):
                        candidate["result"] = "vulnerable"
                        candidate["request"] = self._extract_request_data(driver)
                        self.logger.info(f"Vulnerable: {prepared_candidate_url}") 
                    else:
                        candidate["result"] = "safe"
                        self.logger.info(f"Safe: {prepared_candidate_url}") 
                except TimeoutException as e:
                    candidate["result"] = "script-timeout"
                    self.logger.info(f"Oracle timeout: {prepared_candidate_url}") 
                except Exception as e:
                    error = self._sanatize_str(repr(e))
                    candidate["result"] = f"crash({error})"
                    self.logger.error(f"Crash: {prepared_candidate_url}")
                    driver.close()
                    driver = self._init_driver()
                finally:
                    candidate["time"] = start_time
                    candidates.append(candidate)
                    continue


            driver.close()

            return candidates


    def _extract_request_data(self, driver):
        fn = (
                f"let data = {{}};\n"
                f"data['time'] = document.getElementById('time').textContent;\n"
                f"data['iframe'] = document.getElementById('iframe').textContent;\n"
                f"data['method'] = document.getElementById('method').textContent;\n"
                f"data['url'] = window.location.href;\n"
                f"data['fragment'] = window.location.hash;\n"
                f"data['args'] = document.getElementById('args').textContent;\n"
                f"data['form'] = document.getElementById('form').textContent;\n"
                f"data['json'] = document.getElementById('json').textContent;\n"
                f"data['cookies'] = document.getElementById('cookies').textContent;\n"
                f"data['headers'] = document.getElementById('headers').textContent;\n"
                f"return JSON.stringify(data);\n"
            )
        result = json.loads(driver.execute_script(fn))
        return result

    def _oracle(self, driver, secret):
        fn = (
                f"element = document.getElementById('{secret}');\n"
                f"return element != null;\n"
            )
        result = driver.execute_script(fn)
        return result

    def _sanatize_str(self, error_str):
        return "".join(c if c.isalnum() or c == " " else "." for c in error_str)


