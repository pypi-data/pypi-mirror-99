#!encoding=utf-8
"""
多线程 request http
"""

import sys
import re
import json
import src
from src.regular_utils import AddressPreHandlerUtil
import multiprocessing
from multiprocessing import Pool
import os
import traceback
import time
import pandas as pd
import pdb
import pymongo
import redis
import argparse
from src.decorator.time_decorator import time_out
from src.decorator.time_decorator import timeout_callback


class HttpRequest(object):
    '''
    多线程访问http类
    '''
    def __init__(self):
        pass

    def run_task(self, task, urls, back_func, back_func_err, num):
        '''
        单机运行多线程抓取任务
        '''
        self.p = Pool(num)
        self.p.map_async(self.task, tuple(self.urls), callback=self.back_func, error_callback=self.back_func_err)
        self.p.close()
        self.p.join()

    def task():
        '''
        处理单条url
        '''
        pass
    
    def back_func():
        '''
        处理返回值
        '''
        pass
    
    def back_func_err():
        '''
        处理返回异常
        '''
        pass

if __name__ == "__main__":
    try:
        mHttpHandler = HttpRequest()
        mHttpHandler.run_task(task, urls, back_func, back_func_err, num)
    except:
        traceback.print_exc()
    finally:
        sys.exit(0)

def handler_line(line, outf=None, level="PICK"):
    """
    :function :处理单行
    :parameter outf: 输出mongo
    :parameter line: 输出输入文本
    """
    try:
        global lock
        res = src.baidu_helper.fetch_one(line)
        res_ = json.loads(res)
        res_['source'] = line
        return res_
    except ValueError:
        print("what's up?")
        traceback.print_exc()
        return {"status": "handler_line: Value Error"}
    except ValueError:
        print("what's up?")
        traceback.print_exc()
        return {"status": "handler_line: any other Error"}

'''
返回处理参数
'''
def back_func(values): # 多进程执行完毕会返回所有的结果的列表
    __ = []
    for _ in values:
        try:
            if _ == None:
                continue
            _['action'] = 'suggestion'
            #rediscli.set(_["source"], 1)
            #print(_)
            __.append(_)
        except:
            print("__err__>> ", values)
            traceback.print_exc()
        finally:
            print("__final__", _["source"])
    global lock
    lock.acquire()
    mycoll_out.insert_many(__)
    lock.release()

'''
错误处理回调函数
'''
def back_func_err(values): # 多进程执行完毕会返回所有错误的列表
    print('error', values)

def handler():
    """ 读入所有的地址 """
    try:
        address_words_set = set()
        address_words = []
        NUM = 17
        p = Pool(NUM)
        #mongocli = pymongo.MongoClient("172.20.0.10", 27017)
        mongocli = myclient
        for item in mongocli["db"][coll_in].aggregate([{"$project":{field_name:1,"_id":0}},{"$limit":290000}]):
            if not field_name in item:
                continue
            #_ = item.get("address", "")
            #_ = item["field3"]
            if type(item[field_name]) == str:
                if len(item[field_name]) > 0:
                    address_words_set.add(aphu.sub(item[field_name]))
                    #print(item)
        for _ in list(address_words_set):
            try:
                address_words.append(src.baidu_helper.build_place_v2_suggestion(_, city_name))
            except AttributeError:
                traceback.print_exc()
            except:
                traceback.print_exc()
        matrix_fetch = []
        urls = []
        for index, address_word in enumerate(address_words):
            urls.append(address_word)
            if len(urls) == NUM:
                p.map_async(handler_line, tuple(urls), callback=back_func, error_callback=back_func_err)
                urls = []
        if len(urls) > 0:
            p.map_async(handler_line, tuple(urls), callback=back_func, error_callback=back_func_err)
            matrix_fetch = []
        p.close()
        p.join()
        print("文件处理完毕")
    except FileNotFoundError:
        print("FileNotFoundError")


"""
运行爬取
python3 example_baidu_suggestion.py --input_coll sd_jn --city_name 济南市 --output_coll sd_jn_search_0227 --field address
#python3 example_baidu_suggestion.py --input_coll wj_jq_data_1126 --city_name 吴江区 --output_coll wj_jq_data_1126_suggestion --filed field3
"""

