from abc import abstractmethod


class HtmlParser:

    @abstractmethod
    def parser(self, html):
        pass
