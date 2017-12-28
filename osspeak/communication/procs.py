import time
import asyncio
import asyncio.subprocess
import subprocess
import threading
import json
import sys
from settings import settings
from communication import messages, pubsub, topics

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