import logging
import os
import time
from src import JsonDict
from src import Step, TypePhrase, Sequence


def log_format(name):
    return f"%(asctime)s-{name}-%(levelname)s:\t%(message)s"


class Automaton:
    DEFINED_STEPS = {
        "sequence": Sequence,
        "phrase": TypePhrase
        }

    def __init__(self, name, config=None, path=None):
        self.name = name
        if path is None:
            path = f"config/{name}"
        if not os.path.exists(path):
            os.mkdir(path)
        self.path = path
        if config is None:
            config = f"{path}/{name}.json"
        self.config = JsonDict(json_path=config)
        self.check_config()
        self.steps={}
        self.log = self.set_logger(name)
        self.init_steps()
        self.log.info("Init done")
        self.log.warning("check the logs")

    def check_config(self):
        if "Verbosity" not in self.config:
            self.config["Verbosity"] = logging.DEBUG
        if "step_default" not in self.config:
            self.config["step_default"] = {}
        if "steps" not in self.config:
            self.config["steps"] = [{"type": "sequence", "name": "default_sequence"}]
        if "main_sequence" not in self.config:
            self.config["main_sequence"] = "default_sequence"

    def set_logger(self, name):
        log = logging.getLogger(name)
        formater = logging.Formatter(log_format(name))
        file_handler = logging.FileHandler(f"{self.path}/{self.name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formater)
        log.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.config["Verbosity"])
        console_handler.setFormatter(formater)
        log.addHandler(console_handler)
        log.debug(f"Logger {name} setup")
        return log

    def init_steps(self):
        self.log.debug(f"Init steps Begin")
        for step in self.config["steps"]:
            name = step["name"]
            step_type = step["type"]
            if "config" not in step:
                step["config"] = self.config["step_default"]
            self.steps[name] = self.DEFINED_STEPS[step_type](log=self.set_logger(name), **step)
        self.log.debug(f"Init steps End")

