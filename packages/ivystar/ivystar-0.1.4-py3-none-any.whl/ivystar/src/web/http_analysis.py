#!encoding=utf-8
"""
多线程 request http
"""

import multiprocessing
from multiprocessing import Pool
import sys

# 任务池Pool
global p

class HttpRequest(object):
    '''
    多线程访问http类
    '''
    def __init__(self):
        print('init HttpRequest')

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

    def task(self, tmp_urls):
        '''
        处理单条url
        '''
        try:
          print('run task')
          assert 1 == -1
          return [ValueError,'a']
        except
    
    def back_func(self, values):
        '''
        处理返回值
        '''
        print('run back_func')
        print(values)
    
    def back_func_err(self, values):
        '''
        处理返回异常
        '''
        print('run back_func')
        print(values)

if __name__ == "__main__":
        mHttpHandler = HttpRequest()
        mHttpHandler.run_task(['www.baidu.com','www.sohu.com'], 2)
