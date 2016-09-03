from client import cmdmodule, dispatcher, evtdispatch

def main():
    event_dispatcher = evtdispatch.EventDispatcher()
    event_dispatcher.main_loop()

if __name__ == "__main__":
    main()