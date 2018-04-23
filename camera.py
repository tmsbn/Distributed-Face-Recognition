'''
Camera Module that connects to Docker Nodes to detect a person
Authors:
Thomas Binu
Ruzan Sasuri
Amol Gaikwad
'''


import cv2
import face_recognition
from utils import send_as_json

URL = 'http://127.0.0.1:5001/test_encoding'


def detect_person(rgb_frame):

	print('Loading...')

	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

	if len(face_locations) == 0 and len(face_encodings) == 0:
		return 'No person detected'

	message = {
		'encoding': face_encodings[0].tolist()
	}
	# print(face_encodings[0].tolist())
	response = send_as_json(URL, message)

	return response['result']


def capture_and_detect(vc):

	while True:
		_, im = vc.read()
		rgb_frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

		cv2.imshow('', im)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

		if cv2.waitKey(1) & 0xFF == ord('c'):
			print(detect_person(rgb_frame))

	vc.release()
	cv2.destroyAllWindows()


def main():

	cv2.namedWindow("preview")
	vc = cv2.VideoCapture(0)
	capture_and_detect(vc)



if __name__ == '__main__':
	main()
