#!encoding=utf-8

from ivystar.src.web.http_fetch import HttpRequest
from ivystar.src.web.http_analysis import HttpAnalyze
from ivystar.src.dataio.mongo_helper import MongoHelper
from ivystar.src.conf import MONGO_IP
from ivystar.src.conf import MONGO_PORT
from ivystar.src.conf import SPIDER_LINK
from ivystar.src.conf import SPIDER_SUCC
from ivystar.src.conf import SPIDER_RESULT
from ivystar.src.decorator import prilog
import multiprocessing
from multiprocessing import Pool

global p
global l
global mongo_cli
global ha
ha = HttpAnalyze()
mongo_cli = MongoHelper(MONGO_IP, MONGO_PORT) 
l = multiprocessing.Lock()

class UrlSpider(HttpRequest):

    def __init__(self):
        HttpRequest.__init__(self)

    def run_task(self, urls, num):
        '''
        单机运行多线程抓取任务
        '''
        global p #p不能作为实例变量在进程间传递和序列化。
        p = Pool(num)
        tmp_urls = []
        for url in urls:
            tmp_urls.append(url)
            if len(tmp_urls) == num:
                p.map_async(self.task, tuple(tmp_urls), callback=self.back_func, error_callback=self.back_func_err)
                tmp_urls = []
        p.close()
        p.join()

    def task(self, url):
        global ha
        res = ha(url)
        return res

    def back_func(self, values):
        global l 
        global mongo_cli
        l.acquire()
        for value in values:
            for url in value["links"]:
                mongo_cli.cli["db"][SPIDER_LINK].insert({"url":url})
            mongo_cli.cli["db"][SPIDER_SUCC].insert({"url":value["url"]})
            mongo_cli.cli["db"][SPIDER_RESULT].insert({"url":value["url"], "texts":value["texts"]})
        l.release()
        print("back_func:", values)

    def back_func_err(self, value):
        print("back_func_err:", value)

if __name__ == "__main__":
    mus = UrlSpider()
    NUM = 5
    EPOCH = 10 # 扫描轮数

    ''' 加入原始网站 '''
    for source_url in ["http://www.chinaai.com", "http://www.iteye.com", "https://www.new.qq.com"]:
        mongo_cli.cli["db"][SPIDER_LINK].update_one({"url":source_url}, {"$set":{"url":source_url}}, True)

    ''' 开始扫描 '''
    print([i for i in mongo_cli.cli["db"][SPIDER_LINK].find()])
    for i in range(10):
      urls = []
      for url in mongo_cli.cli["db"][SPIDER_LINK].find({},{"_id":0}):
        if 0 == mongo_cli.cli["db"][SPIDER_SUCC].find({"url":url["url"]},{"_id":0}).count():
          if 'chinaai' in url['url'] or 'iteye' in url["url"] or 'new.qq' in url["url"]:
            urls.append(url["url"])
            print(url["url"])
            if len(urls) == NUM:
              mus.run_task(urls, NUM)
              urls = []

