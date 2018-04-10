from abc import ABC, abstractclassmethod

from PIL import Image


def save(image_file, destination):
    image_file.save(destination)
    return image_file


class AbstractServer(ABC):
    @abstractclassmethod
    def handle_message(self, message):
        """
        :pre: Any implementing methods must return something.
        """
        pass

    @abstractclassmethod
    def handle_image(self, image):
        pass


class DDNNNode(AbstractServer):
    __slots__ = 'save_path'

    def __init__(self):
        self.save_path = 'request.png'

    def handle_message(self, message):
        print(message)
        return '{"message": "got reply"}'

    def handle_image(self, image_file):
        image = Image.open(image_file)
        save(image, self.save_path)
        return '{"message": "got image"}'
