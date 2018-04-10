from PIL import Image
import requests
import json


def echo_message(url, message):
    response = requests.post(url, data=json.dumps(message))
    print(json.loads(response.text))


def echo_image(url, image_name, save_path):
    files = {'media': open(image_name, 'rb')}
    response = requests.post(url, files=files)
    print(json.loads(response.text))
    # save(response.raw, save_path)


def main():
    url = 'http://127.0.0.1:5000/'
    data = dict()
    data['Name'] = 'Ruzan'
    data['Age'] = 27
    data['Status'] = 'Alive'
    echo_message(url + 'user', data)

    image_name = 'elmur.jpg'
    save_path = 'response.png'
    echo_image(url + 'img', image_name, save_path)

if __name__ == '__main__':
    main()