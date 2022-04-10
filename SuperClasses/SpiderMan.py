from abc import ABC, abstractmethod


new_urls = set()
data = {}


class SpiderMan(ABC):

    def __init__(self, url_manager, html_downloader, html_parser, data_store):
        print("111")
        # 调度器内包含其它四个元件，在初始化调度器的时候也要建立四个元件对象的实例
        self.manager = url_manager
        self.downloader = html_downloader
        self.parser = html_parser
        self.data_store = data_store

    # do something at the end
    @abstractmethod
    def callback(self):
        pass

    def spider(self, origin_url):
        # 添加初始url

        global new_urls
        global data
        self.manager.add_new_url(origin_url)
        # 下面进入主循环，暂定爬取页面总数小于100
        num = 0
        while self.manager.has_new_url() and self.manager.continue_scrape():
            try:
                num = num + 1
                print("正在处理第{}个链接".format(num))
                # 从新url仓库中获取url
                new_url = self.manager.get_new_url()
                # 调用html下载器下载页面
                html = self.downloader.download(new_url)
                # 调用解析器解析页面，返回新的url和data
                try:
                    new_urls, data = self.parser.parser(html)
                except Exception as e:
                    print(e)
                for url in new_urls:
                    self.manager.add_new_url(url)
                # 将已经爬取过的这个url添加至老url仓库中
                self.manager.add_old_url(new_url)
                # 将返回的数据存储至文件
                try:
                    self.data_store.store(data)
                    print("store data successfully")
                except Exception as e:
                    print(e)
                print("第{}个链接已经抓取完成".format(self.manager.old_url_size()))
            except Exception as e:
                print(e)
        self.callback()
