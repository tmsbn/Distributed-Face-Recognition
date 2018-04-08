from flask import Flask, request
from abstract_server import DDNNNode

app = Flask(__name__)
message_handler = None


def set_handler(handler):
    global message_handler
    message_handler = handler


@app.route('/test')
def hello_world():
    return 'Hello, World!'


@app.route('/user', methods=['POST'])
def receive_message():
    # if request.method == 'POST':
    # handler = AbstractServer()
    reply = message_handler.handle_message(request.data)
    # print(request.data)
    return reply


def main():
    set_handler(DDNNNode())
    app.run()

if __name__ == '__main__':
    main()