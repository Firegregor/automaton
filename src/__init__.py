from src.json_dict import JsonDict
config = JsonDict(json_path='config/config.json', name="Global")
from src.data import Point, Color, Place
from src.utils import *
from src.steps import Step, TypePhrase
from src.sequence import Sequence
from src.automaton import Automaton
