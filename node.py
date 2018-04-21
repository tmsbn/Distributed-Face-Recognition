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
		log('Assigned node ID:' + str(node_id))
		show_camera()
		get_encodings_from_successor()


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

	log('Transferring encodings to {}'.format(predecessor_node_id))
	for name, face_encoding in face_encodings.items():
		hash_value = get_hash_value(np.asarray(face_encoding))
		log(hash_value)
		# 4 5 8 [10] , [7]
		if is_in_range(node_id, predecessor_node_id, hash_value):
			encodings_to_transfer[name] = face_encoding

	message = {
		'encodings': encodings_to_transfer
	}

	log('Encodings of length {} being transferred from {} to {}:'.format(len(encodings_to_transfer), node_id, predecessor_node_id))

	return json.dumps(message)


# Get encoding from successor
def get_encodings_from_successor():

	global face_encodings, node_id

	if len(nodes) == 0:
		log('No Nodes Yet')
		return
	else:
		print(nodes.keys())

	successor_id = find_successor(node_id, nodes)

	if successor_id == node_id:
		return

	url = nodes[successor_id] + URLS['successor_encodings']

	message = {
		'node_id': node_id
	}

	response = send_as_json(url, message)
	face_encodings = response['encodings']

	log('Encodings after updating:')
	print_encoding_hash_values(face_encodings)
	log("Updated encodings for:" + str(face_encodings.keys()))


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


def start_server():
	threading.Thread(target=app.run, args=(HOST_NAME, PORT)).start()
	time.sleep(0.5)
	# app.run(host=HOST_NAME, port=PORT, debug=True, use_reloader=False)


def main():
	start_server()
	register()


if __name__ == '__main__':
	main()
