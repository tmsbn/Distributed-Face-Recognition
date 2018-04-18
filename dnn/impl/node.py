import json
import socket

import requests
from flask import Flask, request

from dnn.impl.utils import log

SERVER_URL = 'http://172.17.0.2:5000'

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5000
URLS = {
    'client_alive': SERVER_URL + '/alive'
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
    return response


def notify_alive():
    message = {
        'ip': HOST_NAME
    }
    response = send(URLS['client_alive'], message)
    message = json.loads(response.text)
    new_id = message['id']
    if new_id == -1:
        exit()

    global nodes, node_id
    nodes = message['online_nodes']
    node_id = new_id


#  THE FLASK RECEIVERS
@app.route('/online', methods=['POST'])
def set_new_online():
    message = json.loads(request.data)
    nodes[message['id]']] = message['online_node']


#  PRINT ONLINE NODES
def print_online():
    log('ID\tURL')
    for curr_id, url in nodes.iter():
        log(str(curr_id) + '\t' + url)


#  CONTROLLER METHODS
def record_face(image):
    pass


def find_person(person):
    pass


def start_node():
    app.run(host=HOST_NAME, port=PORT)
    notify_alive()
