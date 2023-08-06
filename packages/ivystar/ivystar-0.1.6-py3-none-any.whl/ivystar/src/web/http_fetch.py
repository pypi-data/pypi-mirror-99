#!encoding=utf-8
"""
多线程 request http
"""

import multiprocessing
from multiprocessing import Pool
import sys

# 任务池Pool
global p
global l # nosql没有事务，使用线程锁保证多线程安全
l = multiprocessing.Lock()

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
        print('run task')
        return [ValueError,'a']
    
    def back_func(self, values):
        global l
        l.acquire()
        '''
        处理返回值
        '''
        for value in values:
            print(value)
        l.release()
    
    def back_func_err(self, values):
        '''
        处理返回异常
        '''
        print('run back_func_err:', type(values), values)

if __name__ == "__main__":
    mHttpHandler = HttpRequest()
    mHttpHandler.run_task(['www.baidu.com','www.sohu.com','www.sina.com'], 3)


