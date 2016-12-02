from client import dispatcher
from communication import evtdispatch
from interfaces.cli import menu

def main():
    event_dispatcher = evtdispatch.EventDispatcher()
    event_dispatcher.start_interface()

if __name__ == "__main__":
    main()