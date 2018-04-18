import json

import requests
from flask import Flask, request, make_response

app = Flask(__name__)


def echo_message(url, message):
    response = requests.post(url, data=json.dumps(message))
    print(json.loads(response.text))


@app.route('/test')
def hello_world():
    return 'Hello, World!'


@app.route('/text', methods=['POST'])
def receive_message():
    reply = handle_message(json.loads(request.data))
    print(request.data)
    return make_response(reply)


@app.route('/img', methods=['POST'])
def get_image():
    file = request.files['media']
    print('file', file)
    response = message_handler.handle_image(file)
    return response


def main():
    # set_handler(DDNNNode())
    app.run()


if __name__ == '__main__':
    main()
