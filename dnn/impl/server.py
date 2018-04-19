import json
import socket

import requests
from flask import Flask, request

from dnn.impl.utils import log

HOSTNAME = socket.gethostbyname(socket.gethostname())

NODE_COUNT = 16
app = Flask(__name__)

url_head = 'http://'

URLS = {
    'online': '/online'
}

PORT = 5000

node_id = 0
#  nodes = {'id':'ip'}
nodes = dict()


def send(url, message):
    response = requests.post(url, data=json.dumps(message))
    log(response)
    return response


def send_online_node(live_id):
    message = {
        'id': live_id,
        'url': nodes[live_id]
    }

    for k, v in nodes.items():
        full_url = v + URLS['online']
        send(full_url, message)

#
# #  function to send models.
# # param: List[List]
# def send_models(curr_id, models):
#     message = {
#         'models': models
#     }
#     full_url = nodes[curr_id] + URLS['models']
#     send(full_url, message)


@app.route('/alive', methods=['POST'])
def client_alive():
    alive_id = -1
    for i in range(NODE_COUNT):
        if i not in nodes:
            alive_id = i
            break

    if alive_id != -1:
        ip = json.loads(request.data)['ip']
        nodes[alive_id] = url_head + ip + ':' + PORT
        send_online_node(alive_id)

    message = {'id': alive_id, 'online_nodes': nodes}
    return json.dumps(message)


#  CONTROLLER METHODS
def add_new_person():
    pass


def start_server():
    nodes[node_id] = url_head + HOSTNAME + ':' + PORT
    app.run(host=HOSTNAME, port=5000)

start_server()