'''
Camera Module that connects to Docker Nodes to detect a person
Authors:
Thomas Binu
Ruzan Sasuri
Amol Gaikwad
'''

import grequests
import cv2
import face_recognition
from utils import send_as_json, get_as_json

ONLINE_NODES_URL = 'http://127.0.0.1' + ':5001/online_nodes'
TEST_ENCODING_URL = 'http://127.0.0.1' + ':5002/test_encoding'


def detect_person(rgb_frame, face_locations = [], nodes = []):

	print('Loading...')
	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	if len(face_locations) == 0 and len(face_encodings) == 0:
		return 'No person detected'

	message = {
		'encoding': face_encodings[0].tolist()
	}
	# print(face_encodings[0].tolist())
	response = send_as_json(TEST_ENCODING_URL, message)

	return response['result']


# Get online nodes from server
def get_online_nodes():

	response = get_as_json(ONLINE_NODES_URL)
	nodes = response['nodes']
	return nodes


def capture_and_detect(vc, nodes):

	while True:
		_, im = vc.read()
		rgb_frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

		# face_locations = face_recognition.face_locations(rgb_frame)
		#
		# for (top, right, bottom, left) in face_locations:
		# 	cv2.rectangle(im, (left, top), (right, bottom), (0, 0, 255), 2)

		cv2.imshow('', im)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			print('Quit')
			break

		if cv2.waitKey(1) & 0xFF == ord('c'):
			print(detect_person(rgb_frame))

	vc.release()
	cv2.destroyAllWindows()


def main():

	nodes = []
	# try:
	# 	nodes = get_online_nodes()
	# 	print(nodes)
	# except Exception:
	# 	print('Could not connect to server')
	# 	return

	cv2.namedWindow("preview")
	vc = cv2.VideoCapture(0)
	capture_and_detect(vc, nodes)



if __name__ == '__main__':
	main()
