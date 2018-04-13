NEW_CAMERA = 0
PULL_IMAGES = 1


def new_camera(ip):
    message = dict()
    message['type'] = NEW_CAMERA
    message['ip'] = ip
    return message


def pull_images():
    message = dict()
    message['type'] = PULL_IMAGES
    return message