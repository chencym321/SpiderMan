from abc import ABC, abstractmethod
import threading


class DataStore(ABC):

    # save data
    def __init__(self):
        self.lock = threading.Lock()

    @abstractmethod
    def store(self, data):
        pass
