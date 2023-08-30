import logging
import os
import pyautogui
import time
import keyboard
import win32api, win32con
from src import JsonDict

class Automaton:
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
        self.config["test"] = True

    def click(self,x, y, *args):
        win32api.SetCursorPos( (x, y) )
        if self.config["test"]:
            input('Is mouse in proper place?')
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(self.DELAY)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

