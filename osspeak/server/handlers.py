def dispatch_message_from_client(engine_process, server, msg, *a, **k):
    if not isinstance(msg, bytes):
        msg = msg.encode('utf8')
    if not msg.endswith(b'\n'):
        msg += b'\n'
        engine_process.stdin.write(msg)
        engine_process.stdin.flush()