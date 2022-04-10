from abc import ABC, abstractmethod
from functools import singledispatchmethod


class UrlManager(ABC):

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.processing_urls = set()
        self.failed_urls = set()

    def get_new_url(self):
        url = self.new_urls.pop()
        self.processing_urls.add(url)
        return url

    def has_new_url(self):
        return len(self.new_urls) > 0

    def has_processing_url(self):
        return len(self.processing_urls) > 0

    @singledispatchmethod
    def add_new_url(self, urls: list):
        for url in urls:
            self.add_new_url(url)

    @add_new_url.register
    def _(self, url: str):
        if url not in self.new_urls.union(self.old_urls, self.processing_urls, self.failed_urls):
            self.new_urls.add(url)

    def add_old_url(self, url):
        self.processing_urls.remove(url)
        self.old_urls.add(url)

    def add_failed_url(self, url):
        self.failed_urls.add(url)

    def old_url_size(self):
        return len(self.old_urls)

    def new_url_size(self):
        return len(self.new_urls)

    def processing_url_size(self):
        return len(self.processing_urls)

    def failed_url_size(self):
        return len(self.failed_urls)

    @abstractmethod
    # Tell Spider when to stop scrape
    def continue_scrape(self) -> bool:
        pass
