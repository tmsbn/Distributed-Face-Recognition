import json
import socket
import requests
from flask import Flask, request
from utils import log, find_successor, get_hash_value, send_as_json, is_in_range, print_encoding_hash_values
import threading
import time
import cv2
import face_recognition
import numpy as np
from os.path import join
import glob
import pickle

SERVER_URL = 'http://172.17.0.2:5000'

HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5000
URLS = {
	'register': '/register',
	'models': '/models',
	'model': '/model',
	'test': '/test',
	'successor_encodings': '/successor_encodings'
}

node_id = -1
nodes = dict()  # Key as node id and value as ip address
face_encodings = dict()

app = Flask(__name__)

has_registered = False


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
		print(node_id)
		show_camera()
		get_encodings_from_successor()


# Update face encodings
@app.route('/update_encodings', methods=['POST'])
def update_encodings():
	global nodes, face_encodings

	response = request.get_json(force=True)
	face_encodings = response['encodings']
	for name, face_encoding in face_encodings.items():
		print(name, get_hash_value(np.asarray(face_encoding)))

	message = {
		'success': True
	}
	return json.dumps(message)


# Send encodings to predecessor
@app.route('/update_encodings', methods=['POST'])
def successor_encodings():

	response = request.get_json(force=True)
	predecessor_node_id = response['node_id']
	encodings_to_transfer = {}

	for name, face_encoding in face_encodings:
		hash_value = get_hash_value(np.asarray(face_encoding))

		# 4 5 8 [10] , [7]
		if is_in_range(node_id, predecessor_node_id, hash_value):
			encodings_to_transfer[name] = face_encoding
			face_encodings.pop(name, None)

	message = {
		'encodings': encodings_to_transfer
	}

	log('Encodings being transferred from {} to {}:'.format(node_id, predecessor_node_id))
	print_encoding_hash_values(encodings_to_transfer)

	return json.dumps(message)


# Get encoding from successor
def get_encodings_from_successor():

	global face_encodings

	if len(nodes) == 0:
		log('No Nodes Yet')
		return
	else:
		print(nodes.keys())

	successor_id = str(find_successor(node_id, nodes))

	if int(successor_id) == node_id:
		return

	url = nodes[successor_id] + URLS['successor_encodings']

	message = {
		'node_id': node_id
	}

	response = send_as_json(url, message)
	face_encodings = response['encodings']

	log('Encodings after updating:')
	print_encoding_hash_values(face_encodings)
	log("Updated encodings " + str(face_encodings.keys()))


# Update the list of online nodes
@app.route('/update_online', methods=['POST'])
def update_nodes():
	global nodes, has_registered

	response = request.get_json(force=True)
	nodes = response['nodes']
	log('updating nodes to:' + str(nodes))

	# # Get the encodings from successor after the node has registered
	# if not has_registered:
	#
	# 	has_registered = True

	message = {
		'success': True
	}
	return json.dumps(message)


def start_server():
	threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
	time.sleep(0.5)
	# app.run(host=HOST_NAME, port=PORT, debug=True, use_reloader=False)


def main():
	start_server()
	register()


if __name__ == '__main__':
	main()
