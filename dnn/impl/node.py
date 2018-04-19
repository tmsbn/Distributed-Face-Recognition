import json
import socket

import requests
from flask import Flask, request

from dnn.impl.utils import log

SERVER_URL = 'http://172.17.0.2:5000'

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5000
URLS = {
    'client_alive': '/alive',
    'models': '/models',
    'model': '/model'
}

node_id = -1
nodes = dict()

app = Flask(__name__)


def is_in_range(start, end, curr):
    # (start < end and start <= curr <= end) or (curr >= start or curr <= end)
    if start < end:
        return start <= curr <= end
    else:
        return curr >= start or curr <= end


def send(url, message):
    response = requests.post(url, data=json.dumps(message))
    log(response)
    return json.loads(response.text)


def notify_alive():
    message = {
        'ip': HOST_NAME
    }
    full_url = SERVER_URL + URLS['client_alive']
    message = send(full_url, message)
    new_id = message['id']
    if new_id == -1:
        exit()

    global nodes, node_id
    nodes = message['online_nodes']
    node_id = new_id


#  function to request a models.
#  param: List
def request_models():
    message = {
        'id': node_id
    }
    full_url = SERVER_URL + URLS['models']
    message = send(full_url, message)
    return message['models']


#  function to send a model.
#  param: List
def request_model(url, name):
    message = {
        'id': node_id,
        'name': name
    }
    full_url = url + URLS['model']
    send(full_url, message)


#  THE FLASK RECEIVERS
@app.route('/online', methods=['POST'])
def set_new_online():
    message = json.loads(request.data)
    nodes[message['id']] = message['online_node']


@app.route('/model', methods=['POST'])
def send_model():
    curr_id = json.loads(request.data)['id']
    name = json.loads(request.data)['name']
    model = find_model(name)
    message = {
        'id': curr_id,
        'model': model
    }
    return json.dumps(message)


#  PRINT ONLINE NODES
def print_online():
    log('ID\tURL')
    for curr_id, url in nodes.item():
        log(str(curr_id) + '\t' + url)


# CONTROLLER METHODS
def find_face(image):
    pass


def find_model(name):
    pass


def start_node():
    app.run(host=HOST_NAME, port=PORT)
    notify_alive()
