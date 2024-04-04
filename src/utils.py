import logging
import pyautogui
import time
import keyboard
import win32api, win32con
from typing import Optional
from src import config, Point, Color, Place

DELAY = config["DELAY"]
REGION = config["REGION"]
TILE_LENGTH = config["TILE_LENGTH"]
CONFIDENCE_LEVEL = config["CONFIDENCE_LEVEL"]
EXIT_KEY = config["EXIT_KEY"]

def click(target:Point, hold_time=DELAY, *args, **kwargs) -> None:
    """
    Clicks on point for hold time
    target - Point
    hold_time - (optional) time in seconds, default configured in global config
    Additional arguments will be ignored
    """
    win32api.SetCursorPos(target.as_tuple())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(hold_time)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def doble_click(target:Point, *args, **kwargs) -> None:
    """
    Double clicks on point.
    target - Point
    Additional arguments will be ignored
    """
    win32api.SetCursorPos(target.as_tuple())
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(DELAY)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(DELAY)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(DELAY)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def check_color(target:Point, color:Color, check:str='rgb') -> bool:
    """
    Checks if color in point is exactly as specified
    target - point where check is performed
    color - taget color
    check - string containing "r" "g" or "b" value to check specific channels
    """
    px = pyautogui.pixel(*target.as_tuple())
    ret=False
    if 'r' in check:
        ret = px[0] == color.r
    if 'g'in check:
        ret &= (px[1] == color.g)
    if 'b'in check:
        ret &= (px[2] == color.b)
    return ret

def check_target(target:Place) -> Optional[Point]:
    """
    Returns location of object
    target - Place
    """
    if target.picture:
        box = pyautogui.locateOnScreen(target.picture, confidence=CONFIDENCE_LEVEL)
        if box is None:
            return
        return Point(*box)
    if check_color(target.position, target.color):
        return target.position

def wait_for_picture(self, targets, *args, **kwargs):
    while keyboard.is_pressed(EXIT_KEY) == False:
        for target in targets:
            ret = check_target(target)
            if ret is not None:
                print('found target')
                return ret
        else:
            time.sleep(DELAY)
