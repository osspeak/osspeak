from client import dispatcher
from communication import evtdispatch
from interfaces.cli import menu

def main():
    event_dispatcher = evtdispatch.EventDispatcher()
    menu.Menu(event_dispatcher).prompt_input()
    event_dispatcher.engine_process.shutdown()

if __name__ == "__main__":
    main()