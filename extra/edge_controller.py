import socket

import dnn.demo.messages as msg
from PIL import Image

from extra.const import PATH_TO_IMAGES
from extra.net.Requests_Sender import pull_image_request

HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = '5000'

cameras = []


def save(image_file, destination):
    image_file.save(destination)
    return image_file


class EdgeNode:
    __slots__ = 'save_path'

    def __init__(self):
        self.save_path = PATH_TO_IMAGES + 'request.png'

    def handle_message(self, message):
        if message['type'] == msg.NEW_CAMERA:
            cameras.append(message['ip'])
            print('Added Camera:' + message['ip'])
        return '{"message": "got reply"}'

    def handle_image(self, image_file):
        image = Image.open(image_file)
        save(image, self.save_path)
        return '{"message": "got image"}'


def pull_images():
    for camera in cameras:
        pull_image_request(camera)


def start_edge():
    from extra.net import app, set_handler
    set_handler(EdgeNode())
    app.run(host=HOSTNAME, port=PORT)


start_edge()
