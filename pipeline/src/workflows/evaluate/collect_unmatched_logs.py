import luigi
import json

from ..utils import load_list
from ..utils import load_json
from ..utils import save_json_stream

from uuid import UUID


class CollectUnmatchedLogs(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_dir = luigi.parameter.PathParameter(
            description = "The path to the backend logs."
    )
    src_file_nv_json = luigi.parameter.PathParameter(
            description = "The path to the backend logs."
    )
    src_file_json = luigi.parameter.PathParameter(
            description = "The path to vulnerable candidates."
    )
    out_dir = luigi.parameter.PathParameter(
            description = "The output directory for everything manual analysis."
    )

    #======================================================================
    # Other
    #======================================================================

    def requires(self):
        dependencies = {}
        return dependencies

    def output(self):
        return luigi.LocalTarget(self.out_dir/f"unmatched_logs.json")

    def run(self):
        results = []

        ids = []
        vuln_data = load_json(self.src_file_json)
        not_vuln_data = load_json(self.src_file_nv_json)
        for entry in vuln_data:
            payload = entry["payload"]
            id = self.extract_id(payload)
            if id:
                ids.append(id)

        log_lines = []
        files = self.src_dir.glob("**/*.log")
        for file in files:
            data = load_list(file)
            log_lines += data


        unmatched_lines = []
        for line in log_lines:
            unmatched = True
            for id in ids:
                if id in line:
                    unmatched = False
                    break
            if unmatched:
                unmatched_lines.append(line)


        for line in unmatched_lines:
            data_str = line.split("|")[1].strip()
            try:
                data = json.loads(data_str)
                if not(data["url"] == "https://thesis.test/" and data["method"] == "HEAD"):
                    data["headers"] = json.loads(data["headers"])
                    results.append(data)
            except:
                pass

        unmatched = []

        n = len(results)
        i = 0
        for entry in results:
            print(f"{i/n}% Done")
            i += 1 
            url = entry["url"]
            id = self.extract_id(url)
            if not id:
                continue

            for not_vuln_entry in not_vuln_data:
                payload = not_vuln_entry["payload"]
                if id in payload:
                    entry["client_log"] = not_vuln_entry
                    unmatched.append(entry)

        with self.output().open("w") as file:
            save_json_stream(file, unmatched)

    def extract_id(self, data):
            extracted  = ""
            if "-" not in data:
                return extracted
            id_lower = data.index("-") - 8
            id_upper = data.find(".", id_lower)
            id = data[id_lower:]
            if id_upper > -1:
                id = data[id_lower:id_upper]
            try:
                used_id = UUID(id)
                extracted = str(used_id)
            except:
                pass
            return extracted
