import numpy as np
import requests
import json

LOG = True


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


def is_in_range(start, end, curr):
	# (start < end and start <= curr <= end) or (curr >= start or curr <= end)
	if start < end:
		return start <= curr <= end
	else:
		return curr >= start or curr <= end


def print_online_nodes(nodes):
	for curr_id, url in nodes.items():
		log(str(curr_id) + '\t' + url)


# Calculate hash of the face encoding
def get_hash_value(face_encoding, threshold=0):
	val = np.linalg.norm(face_encoding)
	# print('Original value', val)
	hash_value = int(round((val - 1) * 100)) - threshold
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
		log(get_hash_value(encoding))


# Helper function since keys in  nodes_json are stored as Strings
def get_nodes_from_json_dict(nodes_json):
	nodes = {}
	for key, value in nodes_json.items():
		nodes[int(key)] = value

	return nodes
