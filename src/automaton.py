import logging
import os
import pyautogui
import time
import keyboard
import win32api, win32con
from src import JsonDict

class Automaton:
    LOG_FORMAT = "%(asctime)s-%(name)s-%(levelname)s:\t%(message)s"

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
        if "Verbosity" not in self.config:
            self.config["Verbosity"] = logging.DEBUG
        self.set_logger()
        self.log.info("Init done")
        self.log.warning("check the logs")

    def click(self,x, y, *args):
        win32api.SetCursorPos( (x, y) )
        if self.config["test"]:
            input('Is mouse in proper place?')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(self.DELAY)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        self.log.debug(f"Click at position {x}:{y}")

    def keyboard_output(self, text):
        self.log.debug(f"Simulate typing {text}")
        for x in text:
            keyboard.press(x)
            time.sleep(self.DELAY)

    def set_logger(self):
        self.log = logging.getLogger(self.name)
        formater = logging.Formatter(self.LOG_FORMAT)
        file_handler = logging.FileHandler(f"{self.path}/{self.name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formater)
        self.log.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)# (self.config["Verbosity"])
        console_handler.setFormatter(formater)

        self.log.addHandler(console_handler)
        self.log.debug("Logger setup")

    def run_sequence(self,sequence, exceptions):
        for step in sequence:
            self.log.info(step)
            if self.finished:
                break
            for exc in exceptions:
                exc.check()
            step.run()
