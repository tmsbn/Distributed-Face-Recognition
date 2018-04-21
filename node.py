import json
import socket
import requests
from flask import Flask, request
from utils import log
import threading
import time
import cv2
import face_recognition
import numpy as np
from os.path import join
import glob
import pickle


SERVER_URL = 'http://172.17.0.2:5000'

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5000
URLS = {
    'register': '/register',
    'models': '/models',
    'model': '/model',
    'test': '/test'
}

node_id = -1
nodes = dict()

app = Flask(__name__)


def send(url, message):
    response = requests.post(url, data=json.dumps(message))
    log(response)
    return json.loads(response.text)


# Show camera
def show_camera():
    pass


# Register Node on the server
def register():

    global nodes, node_id

    message = {
        'ip': HOST_NAME
    }
    response = send(SERVER_URL + URLS['register'], message)
    if 'error' in response:
        print(response['error'])
    else:
        node_id = response['id']
        print(node_id)
        show_camera()


@app.route('/update_online', methods=['POST'])
def update_nodes():

    global nodes

    response = request.get_json(force=True)
    nodes = response['nodes']
    print(nodes)
    # print(find_successor(10))

    message = {
        'success': True
    }
    return json.dumps(message)


def find_successor(input_id):

    if not nodes:
        raise ValueError('No nodes registered')

    node_ids = [int(x) for x in nodes.keys()]
    node_ids.sort()
    print('keys', node_ids)

    for curr_id in node_ids:

        if input_id < curr_id:
            return curr_id
    return nodes[0]


def start_server():
    threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
    time.sleep(0.5)
    # app.run(host=HOST_NAME, port=PORT, debug=True, use_reloader=False)


def main():

    start_server()
    register()


if __name__ == '__main__':
    main()
