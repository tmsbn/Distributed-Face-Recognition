from abc import ABC, abstractclassmethod


class AbstractServer(ABC):
    """
    :pre: Any implementing methods must return something.
    """
    @abstractclassmethod
    def handle_message(self, message):
        pass


class DDNNNode(AbstractServer):
    def handle_message(self, message):
        print(message)
        return '{"message": "got reply"}'
