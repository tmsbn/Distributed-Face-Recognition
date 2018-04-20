import json
import socket

import requests
from flask import Flask, request

from utils import log

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
        send(full_url, message)


@app.route('/register', methods=['POST'])
def register():

    alive_id = -1
    for i in range(NODE_COUNT):
        if i not in nodes:
            alive_id = i
            break

    if alive_id != -1:

        ip = json.loads(request.data)['ip']
        nodes[alive_id] = url_head + ip + ':' + PORT
        update_online_nodes()

    message = {'id': alive_id}
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