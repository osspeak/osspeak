import argparse

from client import dispatcher
from communication import evtdispatch
from interfaces.cli import menu

def main():
    clargs = get_args()
    event_dispatcher = evtdispatch.EventDispatcher(clargs)
    event_dispatcher.start_interface()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--interface', default='gui')
    return parser.parse_args()

if __name__ == "__main__":
    main()