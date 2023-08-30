import logging
import sys
from src import Automaton

def main():
    if len(sys.argv) == 1:
        name = "_default"
    else:
        name = sys.argv[1]

    Automaton(name)

if __name__ == "__main__":
    main()

