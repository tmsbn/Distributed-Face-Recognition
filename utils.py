'''
Utility Functions

Authors:
Thomas Binu
Ruzan Sasuri
Amol Gaikwad
'''


import numpy as np
import requests
import json

LOG = True


# Get response from URL as JSON
def get_as_json(url):
	response = requests.get(url)
	log(response)
	return json.loads(response.text)


# Convert message to JSON and send to URL using request object
def send_as_json(url, message):
	response = requests.post(url, data=json.dumps(message))
	log(response)
	return json.loads(response.text)


def send_as_bytes(url, message):
	response = requests.post(url, data=message)
	log(response)
	return message


# Log messages
def log(*messages):
	if LOG:
		for message in messages:
			print(message, end=' ')
		print()


# check if curr is in range between start and end in a circular loop
def is_in_range(start, end, curr, exclude_left=False, exclude_right=False):
	# (start < end and start <= curr <= end) or (curr >= start or curr <= end)
	if start < end:

		if exclude_left:
			return start < curr <= end
		elif exclude_right:
			return start < curr < end
		else:
			return start <= curr <= end
	else:

		if exclude_left:
			return curr > start or curr <= end
		elif exclude_right:
			return curr >= start or curr < end
		else:
			return curr >= start or curr <= end


def print_online_nodes(nodes):
	for curr_id, url in nodes.items():
		log(str(curr_id) + '\t' + url)


# Calculate hash of the face encoding including a threshold
def get_hash_value(face_encoding, threshold=0, mod_space=64):
	val = np.linalg.norm(face_encoding)
	# print('Original value', val)
	hash_value = subtract_mod_space(int(round((val - 1) * 100)), threshold, mod_space)
	return hash_value


def find_successor(input_id, nodes):
	if not nodes:
		raise ValueError('No nodes registered')

	node_ids = [int(x) for x in nodes.keys()]
	node_ids.sort()

	for curr_id in node_ids:

		if input_id < curr_id:
			return curr_id
	return node_ids[0]


def print_encoding_hash_values(encodings):
	for name, encoding in encodings.items():
		log(name, get_hash_value(encoding))


# Helper function since keys in  nodes_json are stored as Strings
def get_nodes_from_json_dict(nodes_json):
	nodes = {}
	for key, value in nodes_json.items():
		nodes[int(key)] = value

	return nodes


# a - b in mod space
def subtract_mod_space(a, b, mod):

	if a < b:
		return (mod + (a - b)) % mod
	else:
		return (a - b) % mod
