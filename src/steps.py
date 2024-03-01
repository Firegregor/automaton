import logging
import pyautogui
import keyboard
import win32api, win32con
from abc import ABC

class Step(ABC):
    LOG_FORMAT = "%(asctime)s-%(name)s-%(levelname)s:\t%(message)s"

    def __init__(self, name, log,**kwargs):
        pass

    def run(self):
        pass

    def export2dict(self):
        pass

class TypePhrase(Step):
    def __init__(self, name, log, **kwargs):
        self.name = name
        self.config = kwargs["config"]
        self.log = log
        if "phrase" in kwargs:
            self.phrase = kwargs["phrase"]
        else:
            self.log.warning("Step {name}: Invalid params")
            self.phrase = None

    def export2dict(self):
        return {"type": phrase, "name":self.name, "phrase":self.phrase}

    def run(self):
        self.log.debug(f"Step {self.name}: typing {self.phrase}")
        if self.phrase is not None:
            for x in self.phrase:
                keyboard.press(x)
                time.sleep(self.DELAY)

