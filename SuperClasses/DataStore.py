from abc import ABC, abstractmethod


class DataStore(ABC):

    # save data
    @abstractmethod
    def store(self, data):
        pass
