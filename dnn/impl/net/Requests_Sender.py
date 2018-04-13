import json
import socket

import requests


from dnn.const.net import PATH_TO_IMAGES
import dnn.impl.net.url_builder as builder
from dnn.demo.messages import new_camera, pull_images


def echo_message(url, message):
    response = requests.post(url, data=json.dumps(message))
    print(json.loads(response.text))


def pull_image_request(ip):
    url = builder.build_text_url_from_ip(ip)
    message = pull_images()
    response = requests.post(url, data=json.dumps(message))
    print(json.loads(response.text))


def add_camera(ip):
    url = builder.build_edge_url()
    message = new_camera(ip)
    response = requests.post(url, data=json.dumps(message))
    print(response)


def upload_image(image_name):
    url = builder.build_edge_image_url()
    files = {'media': open(image_name, 'rb')}
    response = requests.post(url, files=files)
    return json.loads(response.text)


def main():
    url = 'http://127.0.0.1:5000/'
    data = dict()
    data['Name'] = 'Ruzan'
    data['Age'] = 27
    data['Status'] = 'Alive'
    echo_message(url + 'user', data)

    image_name = PATH_TO_IMAGES + 'elmur.jpg'
    upload_image(url + 'img', image_name)

if __name__ == '__main__':
    main()