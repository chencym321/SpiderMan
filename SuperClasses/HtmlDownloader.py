from abc import ABC, abstractmethod


class HtmlDownloader(ABC):

    # return html content as bs4 element or selenium element
    @abstractmethod
    def download(self, url) -> object:
        pass
