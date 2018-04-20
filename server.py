import json
import socket

import requests
from flask import Flask, request

from utils import log
import time

HOSTNAME = socket.gethostbyname(socket.gethostname())


NODE_COUNT = 32
app = Flask(__name__)


url_head = 'http://'

URLS = {
    'update_online': '/update_online'
}

PORT = 5000

node_id = 0
nodes = dict()


def send(url, message):
    response = requests.post(url, data=json.dumps(message))
    log(response)
    return response


def update_online_nodes():

    message = {
        'nodes': nodes
    }

    for key, value in nodes.items():

        full_url = value + URLS['update_online']
        log(str(key) + " " + full_url)
        # time.sleep(0.5)
        send(full_url, message)


@app.route('/register', methods=['POST'])
def register():

    try:
        register_id = -1
        for i in range(NODE_COUNT):
            if i not in nodes:
                register_id = i
                break

        if register_id != -1:

            ip = json.loads(request.data)['ip']
            nodes[register_id] = url_head + ip + ':' + str(PORT)
            update_online_nodes()

    except:
        message = {'error': 'Could not send message'}
        return json.dumps(message)

    message = {'id': register_id}
    return json.dumps(message)


@app.route('/test', methods=['POST'])
def test_message():
    print(json.loads(request.data))
    return request.data


def start_server():
    app.run(host=HOSTNAME, port=5000, debug=True, use_reloader=False)


def main():
    start_server()


if __name__ == '__main__':
    main()