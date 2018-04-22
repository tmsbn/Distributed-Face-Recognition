import json
import socket
import requests
import random
from flask import Flask, request
from utils import log, find_successor, get_hash_value, send_as_json, send_as_bytes
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
from collections import defaultdict
from PIL import Image

HOST_NAME = socket.gethostbyname(socket.gethostname())


NODE_COUNT = 32
app = Flask(__name__)


url_head = 'http://'

URLS = {
    'update_online': '/update_online',
    'update_encodings': '/update_encodings'
}

PORT = 5000

nodes = dict()

train_image_encodings = {}


# Calculate the face encodings of images and store in server
def train_models_in_system():

    global train_image_encodings

    train_images_dir = join("images", "train")
    train_image_files = glob.glob(join(train_images_dir, "*.jpg"))

    log('Loading images from server')

    for train_image_file in train_image_files:

        train_image = face_recognition.load_image_file(train_image_file)
        train_image_encoding = face_recognition.face_encodings(train_image)
        train_image_name = train_image_file.split("/")[-1].split(".")[0]

        if len(train_image_encoding) > 0:
            train_image_encodings[train_image_name] = train_image_encoding[0].tolist()

    for name, face_encoding in train_image_encodings.items():
        log(name + ":" + str(get_hash_value(face_encoding)))


def send_encodings_to_node(node_id):
    message = {
        'encodings': train_image_encodings
    }

    url = nodes[node_id] + URLS['update_encodings']
    send_as_json(url, message)


# Generate random node id
def get_new_node_id():

    register_id = -1
    exists = True
    while exists:
        register_id = random.randint(1, NODE_COUNT + 1)
        if register_id not in nodes:
            exists = False

    return register_id


def update_online_nodes():

    message = {
        'nodes': nodes
    }

    log('Node List')
    for key, value in nodes.items():

        full_url = value + URLS['update_online']
        log(str(key) + " " + full_url)
        send_as_json(full_url, message)


@app.route('/register', methods=['POST'])
def register():

    try:
        register_id = get_new_node_id()

        if register_id != -1:
            response = request.get_json(force=True)
            ip = response['ip']
            nodes[register_id] = url_head + ip + ':' + str(PORT)
            update_online_nodes()

        if len(nodes) == 1:
            send_encodings_to_node(register_id)

    except Exception as e:

        traceback.print_exc()
        message = {'error': 'Could not send'}
        return json.dumps(message)

    message = {'id': register_id}
    return json.dumps(message)


@app.route('/test', methods=['POST'])
def test_message():

    response = request.get_json(force=True)
    message = response['message']
    return json.dump(message)


def start_server():
    threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
    time.sleep(0.5)


def main():
    train_models_in_system()
    start_server()


if __name__ == '__main__':
    main()