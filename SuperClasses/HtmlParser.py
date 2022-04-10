from abc import ABC, abstractmethod


class HtmlParser(ABC):

    # parse html and return new_urls as set of new url and data to store
    @abstractmethod
    def parser(self, html) -> (list, list):
        pass
