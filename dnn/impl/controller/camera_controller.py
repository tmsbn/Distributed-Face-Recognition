import socket

from Pillow import Image

import dnn.demo.messages as msg
from dnn.const.net import PATH_TO_IMAGES
from dnn.impl.net.Requests_Sender import add_camera, upload_image

HOSTNAME = socket.gethostbyname(socket.gethostname())
PORT = '5000'
URL = 'http://' + HOSTNAME + PORT

cameras = []


def save(image_file, destination):
    image_file.save(destination)
    return image_file


class CameraNode:
    __slots__ = 'save_path'

    def __init__(self):
        self.save_path = PATH_TO_IMAGES + 'request.png'

    def handle_message(self, message):
        if message['type'] == msg.PULL_IMAGES:
            take_and_send_image()
        return '{"message": "taking image"}'

        # def handle_image(self, image_file):
        #     image = Image.open(image_file)
        #     save(image, self.save_path)
        #     return '{"message": "got image"}'


def take_and_send_image():
    print('You have been shot by a camera')
    upload_image(PATH_TO_IMAGES + 'elmur.jpg')  # The image file. Better to save and send than just send.


def start_camera():
    # take_and_send_image()
    # return
    from dnn.impl.net.Flask_Receiver import app, set_handler
    set_handler(CameraNode())

    # add_camera(HOSTNAME)
    app.run(host=HOSTNAME, port=PORT)


start_camera()
