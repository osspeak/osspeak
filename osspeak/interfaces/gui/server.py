from flask import Flask, jsonify
import queue
from communication import common, messages

app = Flask(__name__)
server_message_queue = queue.Queue(maxsize=10)
messages.subscribe(messages.MESSAGE_GUI, lambda msg: common.put_message_in_queue(server_message_queue, msg))

@app.route('/poll')
def poll():
    msg = server_message_queue.get()
    return jsonify(msg)