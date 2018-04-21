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
import threading

HOST_NAME = socket.gethostbyname(socket.gethostname())


NODE_COUNT = 32
app = Flask(__name__)


url_head = 'http://'

URLS = {
    'update_online': '/update_online'
}

PORT = 5000

node_id = 0
nodes = dict()

train_image_encodings = {}


def send(url, message):
    response = requests.post(url, data=json.dumps(message))
    log(response)
    return response


# Calculate hash of the face encoding
def get_hash_value(face_encoding, threshold=0):

    val = np.linalg.norm(face_encoding)
    print('Original value', val)
    hash_value = int(round((val - 1) * 100)) - threshold
    return hash_value


def train_models_in_system():

    global train_image_encodings

    train_images_dir = join("images", "train")
    train_image_files = glob.glob(join(train_images_dir, "*.jpg"))

    for train_image_file in train_image_files:
        train_image = face_recognition.load_image_file(train_image_file)
        train_image_encoding = face_recognition.face_encodings(train_image)
        train_image_name = train_image_file.split("/")[-1].split(".")[0]

        if len(train_image_encoding) > 0:
            train_image_encodings[train_image_name] = train_image_encoding[0]
            print(get_hash_value(train_image_encoding[0]))


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
    threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
    time.sleep(0.5)


def main():
    train_models_in_system()
    start_server()


if __name__ == '__main__':
    main()