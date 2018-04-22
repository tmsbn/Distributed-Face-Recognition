import cv2
import face_recognition
from utils import send_as_json

URL = 'http://127.0.0.1:5001/test_encoding'


def detect_person(rgb_frame):

	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
	message = {
		'encoding': face_encodings[0].tolist()
	}
	print(face_encodings[0].tolist())
	response = send_as_json(URL, message)

	print(response['result'])


def get_frame_from_camera(vc):
	_, im = vc.read()
	rgb_frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
	return rgb_frame


def main():

	cv2.namedWindow("preview")
	vc = cv2.VideoCapture(0)
	rgb_frame = get_frame_from_camera(vc)
	detect_person(rgb_frame)


if __name__ == '__main__':
	main()
