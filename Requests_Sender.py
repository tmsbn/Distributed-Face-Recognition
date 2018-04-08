import requests
import json


def echo_message(url, message):
    response = requests.post(url, data=json.dumps(message))
# get(url, data=data)
    print(json.loads(response.text))


def main():
    url = 'http://127.0.0.1:5000/user'

    data = dict()
    data['Name'] = 'Ruzan'
    data['Age'] = 27
    data['Status'] = 'Alive'
    echo_message(url, data)

if __name__ == '__main__':
    main()