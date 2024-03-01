import logging
import pyautogui
import keyboard
import win32api, win32con
from src import Step

class Sequence(Step):
    def __init__(self, name, log, **kwargs):
        self.__name = name
        self.config = kwargs["config"]
        self.log = log
        if "steps" not in kwargs:
            self.__steps = []
        else:
            self.__steps = kwargs["steps"]
        if "conditional" not in kwargs:
            self._conditional = []
        else:
            self._conditional = kwargs["conditional"]

    def add_step(self, step):
        pass

    def click(self,x, y, *args):
        win32api.SetCursorPos( (x, y) )
        if self.config["test"]:
            input('Is mouse in proper place?')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(self.DELAY)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        self.log.debug(f"Click at position {x}:{y}")

    def run(self):
        for step in self.__steps:
            self.log.info(step)
            if self.finished:
                break
            for exc in self._conditional:
                exc.check()
            step.run()
