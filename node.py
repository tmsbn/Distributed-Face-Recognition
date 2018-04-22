import json
import socket
import requests
from flask import Flask, request
from utils import log, find_successor, get_hash_value, send_as_json, is_in_range, print_encoding_hash_values, get_nodes_from_json_dict
import threading
import time
import cv2
import face_recognition
import numpy as np
from os.path import join, exists
import glob
import pickle
from resizeimage import resizeimage

SERVER_URL = 'http://172.17.0.2:5000'

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5000
URLS = {
	'register': '/register',
	'models': '/models',
	'model': '/model',
	'test': '/test',
	'successor_encodings': '/successor_encodings',
	'search_image' : '/search_image'
}

node_id = -1
nodes = dict()  # Key as node id and value as ip address
face_encodings = dict()

app = Flask(__name__)

has_registered = False

SENSITIVITY = 2

IMAGE_WIDTH = 1000
IMAGE_HEIGHT = 1000


# Show camera
def show_camera():
	pass


# Register Node on the server
def register():
	global nodes, node_id

	message = {
		'ip': HOST_NAME
	}
	response = send_as_json(SERVER_URL + URLS['register'], message)
	if 'error' in response:
		print(response['error'])
	else:
		node_id = response['id']
		log('Assigned node ID:' + str(node_id))
		show_camera()
		get_encodings_from_successor()


# Search Images
@app.route('/search_image', methods=['POST'])
def search_image():

	global nodes, face_encodings
	response = request.get_json(force=True)
	unknown_face_encoding = np.asarray(response['encoding'])

	message = {
		'name': search_encodings(unknown_face_encoding)
	}

	return json.dumps(message)


def search_encodings(unknown_face_encoding):

	log('Comparing face distances')
	for name, face_encoding in face_encodings.items():
		face_distances = face_recognition.face_distance([face_encoding], unknown_face_encoding)
		log('face distance', face_distances, name)
		if face_distances[0] <= 0.5:
			return name

	return ''


# Update face encodings
@app.route('/update_encodings', methods=['POST'])
def update_encodings():
	global nodes, face_encodings

	log('Updated Encodings from Server')
	response = request.get_json(force=True)
	face_encodings = response['encodings']
	for name, face_encoding in face_encodings.items():
		log(name + ':' + str(get_hash_value(np.asarray(face_encoding))))

	message = {
		'success': True
	}
	return json.dumps(message)


# Send encodings to predecessor
@app.route('/successor_encodings', methods=['POST'])
def successor_encodings():

	response = request.get_json(force=True)
	predecessor_node_id = int(response['node_id'])
	encodings_to_transfer = {}

	log('Transferring encodings from {} to {}'.format(node_id, predecessor_node_id))
	for name, face_encoding in face_encodings.items():
		hash_value = get_hash_value(np.asarray(face_encoding))

		if is_in_range(node_id, predecessor_node_id, hash_value):
			encodings_to_transfer[name] = face_encoding
			log(name + ':' + str(get_hash_value(np.asarray(face_encoding))))

	message = {
		'encodings': encodings_to_transfer
	}

	return json.dumps(message)


# Get encoding from successor
def get_encodings_from_successor():

	global face_encodings, node_id

	if len(nodes) == 0:
		log('No Nodes Yet')
		return

	successor_id = find_successor(node_id, nodes)

	if successor_id == node_id:
		return

	url = nodes[successor_id] + URLS['successor_encodings']

	message = {
		'node_id': node_id
	}

	response = send_as_json(url, message)
	face_encodings = response['encodings']

	log('Encodings after update from {}:'.format(successor_id))
	print_encoding_hash_values(face_encodings)


# Update the list of online nodes
@app.route('/update_online', methods=['POST'])
def update_nodes():
	global nodes, has_registered

	response = request.get_json(force=True)
	nodes_json = response['nodes']
	nodes = get_nodes_from_json_dict(nodes_json)
	log('updating nodes to:' + str(nodes))

	message = {
		'success': True
	}
	return json.dumps(message)


# Search encoding in node
def search_encoding_in_nodes(test_image_encoding):

	hash_value = get_hash_value(test_image_encoding, 5)  # Add threshold
	log(hash_value)
	count = 0

	while count < SENSITIVITY:
		log('some loop issue')
		successor_node_id = find_successor(hash_value, nodes)

		if successor_node_id == node_id:  # If its the same node, search the node and return the value
			return 'Welcome ' + search_encodings(test_image_encoding)

		message = {
			'encoding': test_image_encoding.tolist(),
			'count': count
		}

		url = nodes[successor_node_id] + URLS['search_image']
		response = send_as_json(url, message)
		log('Stuck here')
		if response['name'] == '':
			hash_value = successor_node_id
			count += 1
		else:
			return 'Welcome ' + response['name']

	return 'Person not found'


# Search for image , this function will be modified to fit in a camera
def search_image_from_user():

	image_name = input('Enter image name to search:')
	image_name = image_name + '.jpg'
	image_path = join("images", 'test', image_name)
	if exists(image_path):
		test_image = face_recognition.load_image_file(image_path)
		# test_image = resizeimage.resize_cover(test_image, [IMAGE_WIDTH, IMAGE_HEIGHT])
		test_image_encoding = face_recognition.face_encodings(test_image)[0]

		result = search_encoding_in_nodes(test_image_encoding)
		print(result)

	else:
		print('No such image found')


@app.route('/test_encoding', methods=['POST'])
def test_encoding():

	log('Requested for encoding search...')
	request_json = request.get_json(force=True)
	encoding = request_json['encoding']
	log('Client encoding', encoding)
	search_result = search_encoding_in_nodes(np.asarray(encoding))
	message = {
		'result': search_result
	}
	return json.dumps(message)


@app.route('/')
def hello_world():
	return 'Dockerized'


def start_server():
	threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
	time.sleep(0.5)


def main():
	start_server()
	register()
	search_image_from_user()


if __name__ == '__main__':
	main()
