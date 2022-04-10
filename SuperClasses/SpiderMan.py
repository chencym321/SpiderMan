#                    _ooOoo_
#                   o8888888o
#                   88" . "88
#                   (| -_- |)
#                    O\ = /O
#                ____/`---'\____
#              .   ' \\| |// `.
#               / \\||| : |||// \
#             / _||||| -:- |||||- \
#               | | \\\ - /// | |
#             | \_| ''\---/'' | |
#              \ .-\__ `-` ___/-. /
#           ___`. .' /--.--\ `. . __
#        ."" '< `.___\_<|>_/___.' >'"".
#       | | : `- \`.;`\ _ /`;.`/ - ` : | |
#         \ \ `-. \_ __\ /__ _/ .-` / /
# ======`-.____`-.___\_____/___.-`____.-'======
#                    `=---='
#
# .............................................
#          佛祖保佑             永无BUG


from abc import ABC, abstractmethod
import threading
import queue


new_urls = set()
data = {}


def ordinal(n):
    if 11 <= n <= 13:
        return str(n) + 'th'
    elif n % 10 == 1:
        return str(n) + 'st'
    elif n % 10 == 2:
        return str(n) + 'nd'
    elif n % 10 == 3:
        return str(n) + 'rd'
    else:
        return str(n) + 'th'


class SpiderMan(ABC):

    def __init__(self, url_manager, html_downloader, html_parser, data_store):
        # Instantiate  UrlManager, HtmlDownloader, HtmlParser and DataStore and assigned to SpiderMan instance
        self.manager = url_manager
        self.downloader = html_downloader
        self.parser = html_parser
        self.data_store = data_store

    # do something at the end (optional)
    @abstractmethod
    def callback(self):
        pass

    # called when url failed to process
    @abstractmethod
    def error_logging(self):
        pass

    def process_url(self, url):
        global new_urls
        global data
        try:
            # download html as bs4 or selenium
            html = self.downloader.download(url)
            # parse html and return new urls and data
            new_urls, data = self.parser.parser(html)
            # add new urls parsed from html
            self.manager.add_new_url(new_urls)
            # add processed url to old_url
            self.manager.add_old_url(url)
            # save data
            self.data_store.store(data)
        except Exception as e:
            self.manager.add_failed_url(url)
            print(e)

    def consume(self, producer, thread_no, timeout=5):
        while self.manager.has_new_url() or self.manager.has_processing_url() or not producer.empty():
            try:
                task = producer.get(True, timeout=timeout)
            except queue.Empty:
                continue
            url = task['url']
            num = task['num']
            print(f"Worker {thread_no} processing {ordinal(num)} url: {url}")
            self.process_url(url)
            producer.task_done()
            print(f"Worker {thread_no} processed {ordinal(num)} url : pending url: {self.manager.new_url_size()} "
                  f"processing url: {self.manager.processing_url_size()} processed url: {self.manager.old_url_size()}")

    def spider(self, origin_urls, no_threads=10):
        # add origin urls
        self.manager.add_new_url(origin_urls)

        print(f'{len(origin_urls)} origin urls added!')
        num = 0
        producer_queue = queue.Queue()
        # start consumer threads
        for i in range(no_threads):
            consumer = threading.Thread(target=self.consume, args=(producer_queue, i,), daemon=True)
            consumer.start()
        # start looping
        while (self.manager.has_new_url() or self.manager.has_processing_url()) and self.manager.continue_scrape():
            # get new url from url manager
            new_url = self.manager.get_new_url()
            num = num + 1
            # add task to queue
            producer_queue.put({"url": new_url, "num": num})

        producer_queue.join()
        print(f"\n#######################################\n{self.manager.old_url_size()} urls processed.")
        if self.manager.failed_url_size() > 0:
            self.error_logging()
        self.callback()
