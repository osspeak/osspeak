import socket
import locale
import sys
import subprocess
import time
from asyncio.subprocess import PIPE
import xml.etree.ElementTree as ET
sys.path.append("..")
# sys.path.append(r'C:\Users\evan\modules\osspeak\sprecgrammars')
from osspeak import protocols, defaults
import threading
from osspeak.client import cmdmodule, dispatcher, evtdispatch
from osspeak.communication import guimanager
import pprint

def main():

    # messenger = protocols.SocketMessenger(port=defaults.CLIENT_PORT, other_port=defaults.SERVER_PORT)
    # msg_dispatcher = dispatcher.SingleProcessMessageDispatcher()
    event_dispatcher = evtdispatch.EventDispatcher()
    event_dispatcher.main_loop()
    # try:
    #     # msg_dispatcher.gui_manager = guimanager.GuiManager()
    #     # msg_dispatcher.gui_manager.launch()
    #     msg_dispatcher.cmd_module_loader = cmdmodule.CommandModuleWatcher()
    #     msg_dispatcher.cmd_module_loader.load_command_json()
    #     msg_dispatcher.cmd_module_loader.create_grammar_nodes()
    #     grammar = msg_dispatcher.cmd_module_loader.build_srgs_xml_grammar()
    #     msg = 'grammar_content {}'.format(ET.tostring(grammar).decode('utf8'))
    #     # messenger.send_message(msg)
    #     msg_dispatcher.message_engine(msg)
    #     input('Press the any key: ')
    # finally:
    #     msg_dispatcher.cleanup()


if __name__ == "__main__":
    main()