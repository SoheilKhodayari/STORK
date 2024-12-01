import luigi

from workflows.collect.wayback import CollectAll
from workflows.logging import configure_logging

if __name__ == "__main__":

    configure_logging()

    config_path = "configs/debug.cfg"

    config = luigi.configuration.get_config()
    config.read(config_path)

    tasks = [CollectAll()]
    luigi.build(tasks, workers=1, local_scheduler=True)
