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

    def process_url(self, url, num):
        global new_urls
        global data
        try:
            print(f"Processing {ordinal(num)} url: {url}")
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
            print(f"{ordinal(num)} url processed: {url}")
        except Exception as e:
            print(e)

    def spider(self, origin_urls):
        # add origin urls
        self.manager.add_new_url(origin_urls)

        print(f'{len(origin_urls)} origin urls added!')
        # start looping
        num = 0
        processing_threads = []
        while self.manager.has_new_url() and self.manager.continue_scrape():
            # get new url from url manager
            new_url = self.manager.get_new_url()
            num = num + 1
            processing_thread = threading.Thread(target=self.process_url, args=(new_url, num,))
            processing_thread.start()
            processing_threads.append(processing_thread)
        print("\n#######################################\nNo more new url, waiting for existing process to finish.")
        for pthread in processing_threads:
            if pthread.is_alive():
                pthread.join()
        print("\n#######################################\nAll urls processed.")
        self.callback()
