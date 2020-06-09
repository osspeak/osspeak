import time
import asyncio
import asyncio.subprocess
import subprocess
import threading
import json
import sys
from settings import settings
from communication import pubsub, topics

class ThreadedProcessHandler:

    def __init__(self, *args, on_output=None):
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        self.on_output = on_output
        self.start_listening()
        
    def send_message(self, msg):
        if not isinstance(msg, bytes):
            msg = msg.encode('utf8')
        if not msg.endswith(b'\n'):
            msg += b'\n'
        self.process.stdin.write(msg)
        try:
            self.process.stdin.flush()
        except OSError:
            print(f'Process {self} already closed')

    def dispatch_process_output(self):
        for line in self.process.stdout:
            line = line.decode('utf8')
            self.on_output(line)

    def dispatch_process_error(self):
        for line in self.process.stderr:
            line = line.decode('utf8')
            print('error: ', line)

    def start_listening(self):
        threading.Thread(target=self.dispatch_process_output, daemon=True).start()
        threading.Thread(target=self.dispatch_process_error, daemon=True).start()

class ProcessHandler:

    @classmethod
    async def create(cls, *args, **kw):
        process_instance = cls(**kw)
        create = asyncio.create_subprocess_exec(
            *args,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        process_instance.process = await create
        asyncio.ensure_future(process_instance.dispatch_process_output())
        asyncio.ensure_future(process_instance.dispatch_process_err())
        return process_instance

    def __init__(self, on_output=None, on_exit=None):
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
        if self.on_exit is not None:
            await self.on_exit()
            
    async def dispatch_process_err(self):
        async for line in self.process.stderr:
            line = line.decode('utf8')
            print('error: ', line)