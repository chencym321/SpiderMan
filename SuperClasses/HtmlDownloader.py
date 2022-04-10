from abc import abstractmethod


class HtmlDownloader:

    @abstractmethod
    def download(self, url):
        pass
