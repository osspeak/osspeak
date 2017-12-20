import time
import asyncio
import asyncio.subprocess
import subprocess
import threading
import json
import sys
from settings import settings
import xml.etree.ElementTree as ET
from communication import messages, pubsub, topics

if getattr(sys, 'frozen', False):
    ENGINE_PATH = r'engines\wsr\RecognizerIO.exe'
else:
    ENGINE_PATH = r'..\engines\RecognizerIO\RecognizerIO\bin\Debug\RecognizerIO.exe'

class ProcessHandler:

    @classmethod
    async def create(cls, path, *a, **kw):
        process_instance = cls(path, *a, **kw)
        create = asyncio.create_subprocess_exec(
            path,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        process_instance.process = await create
        asyncio.ensure_future(process_instance.dispatch_process_output())
        return process_instance

    def __init__(self, path, on_output=None, on_exit=lambda: None):
        self.on_output = on_output
        self.on_exit = on_exit
        self.process = None

    def kill(self):
        self.process.kill()
        
    async def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        try:
            await self.process.stdin.drain()
        except OSError:
            print(f'Process {self} already closed')

    async def dispatch_process_output(self):
        async for line in self.process.stdout:
            line = line.decode('utf8')
            await self.on_output(line)

