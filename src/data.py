import pyautogui
from enum import Enum
from dataclasses import dataclass
from typing import Optional


@dataclass
class Point:
    x:int
    y:int

    def offset(self, x, y):
        return Point(self.x +x, self.y+y)

    def as_tuple(self) -> tuple:
        return self.x, self.y

@dataclass
class Color:
    r:int
    g:int
    b:int

    @classmethod
    def from_place(cls, place):
        return cls(*pyautogui.pixel(*place.point))

    def mean(self) -> int:
        return (self.r +self.g + self.b) // 3

    def __gt__(self, other) -> bool:
        if other is None:
            return True
        return self.mean() >= other.mean()


@dataclass
class Place:
    picture: str
    position: Point
    color:tuple = None

    @property
    def point(self):
        return self.position.as_tuple()

