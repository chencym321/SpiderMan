from abc import ABC, abstractmethod


class UrlManager(ABC):

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()
        self.processing_urls = set()
        self.failed_url = set()

    def get_new_url(self):
        url = self.new_urls.pop()
        self.processing_urls.add(url)
        return url

    def has_new_url(self):
        return len(self.new_urls) > 0

    def has_processing_url(self):
        return len(self.processing_urls) > 0

    def add_new_url(self, url):
        self.new_urls.update(url)

    def add_old_url(self, url):
        self.processing_urls.remove(url)
        self.old_urls.add(url)

    def add_failed_url(self, url):
        self.failed_url.add(url)

    def old_url_size(self):
        return len(self.old_urls)

    def new_url_size(self):
        return len(self.new_urls)

    def processing_url_size(self):
        return len(self.processing_urls)

    def failed_url_size(self):
        return len(self.failed_url)

    @abstractmethod
    # Tell Spider when to stop scrape
    def continue_scrape(self) -> bool:
        pass
