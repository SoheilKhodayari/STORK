import luigi
import json

from ..utils import load_json
from ..utils import save_json_stream


class CollectVulnerable(luigi.Task):

    #======================================================================
    # Files and Directories
    #======================================================================
    src_dir = luigi.parameter.PathParameter(
            description = "The path to the dir containing the evaluation logs."
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
        return luigi.LocalTarget(self.out_dir/f"vulnerable.json")

    def run(self):
        entries = []
        results = self.src_dir.glob("**/results.json")
        for file in results:
            data = load_json(file)
            for entry in data:
                if entry["result"] == "vulnerable":
                    headers = entry["request"]["headers"]
                    if isinstance(headers, str):
                        entry["request"]["headers"] = json.loads(headers)
                    entries.append(entry)
        with self.output().open("w") as file:
            save_json_stream(file, entries)
