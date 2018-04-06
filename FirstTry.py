from flask import Flask, url_for, request
app = Flask(__name__)


data = ''


@app.route('/test')
def hello_world():
    return 'Hello, World!'


@app.route('/user', methods=['POST'])
def receive_message():
    # if request.method == 'POST':
    print(request.data)
    return request.data


def get_urls():
    url_dict = dict()
    with app.test_request_context():
        url_dict['hello_world'] = url_for('hello_world')
        url_dict['receive_message'] = url_for('receive_message', message="Something")
    return url_dict


def send_message(message):
    send_url = url_for('receive_message', message=message)

app.run()


