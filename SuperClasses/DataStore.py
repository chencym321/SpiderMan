from abc import abstractmethod


class DataStore:

    @abstractmethod
    def store(self, html):
        pass
