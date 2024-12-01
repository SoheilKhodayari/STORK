import yaml
import pathlib
import logging
from logging import config as logging_config

def get_logger(name):
    return logging.getLogger(name.split(".")[0])

def configure_logging():
    config_file = "logging.yaml"
    config_path = (pathlib.Path(__file__).parent/config_file).as_posix()
    with open(config_path, "r") as f:
        config = yaml.safe_load(f.read())
        logging_config.dictConfig(config)
