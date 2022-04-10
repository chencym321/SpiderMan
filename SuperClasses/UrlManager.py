class UrlManager:

    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def add_new_url(self, url):
        self.new_urls.update(url)

    def has_new_url(self):
        return len(self.new_urls) > 0

    def get_new_url(self):
        return self.new_urls.pop()

    def add_old_url(self, url):
        self.old_urls.update(url)

    def old_url_size(self):
        return len(self.old_urls)
