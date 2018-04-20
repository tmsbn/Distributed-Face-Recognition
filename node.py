import json
import socket
import requests
from flask import Flask, request
from utils import log
import threading


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


@app.route('/update_online', methods=['POST'])
def update_nodes():

    global nodes

    response = json.loads(request.data)
    nodes = response['nodes']
    print(nodes)
    return None


def start_server():
    threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
    # app.run(host=HOST_NAME, port=PORT, debug=True, use_reloader=False)


def main():

    start_server()
    register()



if __name__ == '__main__':
    main()
