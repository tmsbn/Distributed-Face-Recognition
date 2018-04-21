import json
import socket
import requests
import random
from flask import Flask, request
from utils import log
from requests import exceptions
import time
import cv2
import face_recognition
import numpy as np
from os.path import join
import glob
import pickle
import traceback

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


# Generate random node id
def get_new_node_id():

    register_id = -1
    exists = True
    while exists:
        register_id = random.randint(1, NODE_COUNT + 1)
        if node_id not in nodes:
            exists = False

    return register_id


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
        register_id = get_new_node_id()

        if register_id != -1:
            response = request.get_json(force=True)
            ip = response['ip']
            nodes[register_id] = url_head + ip + ':' + str(PORT)
            update_online_nodes()

    except Exception as e:
        traceback.print_exc()
        message = {'error': 'Could not send'}
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