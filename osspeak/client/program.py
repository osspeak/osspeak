import socket
import locale
import sys
import subprocess
import time
from asyncio.subprocess import PIPE
from contextlib import closing
import xml.etree.ElementTree as ET
sys.path.append("..")
# sys.path.append(r'C:\Users\evan\modules\osspeak\sprecgrammars')
from osspeak import protocols, defaults
import asyncore
import time
import threading
from osspeak.client import cmdmodule
import pprint

def main():

    messenger = protocols.SocketMessenger(port=defaults.CLIENT_PORT, other_port=defaults.SERVER_PORT)
    try:
        cmd_module_loader = cmdmodule.CommandModuleHandler()
        cmd_module_loader.load_command_json()
        grammar = cmd_module_loader.build_srgs_xml_grammar()
        msg = 'grammar_content {}'.format(ET.tostring(grammar).decode('utf8'))
        print(msg)
        messenger.send_message(msg)
    finally:
        messenger.cleanup()


if __name__ == "__main__":
    main()