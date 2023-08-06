#encoding=utf-8
# ================================================================
#   Copyright (C) 2020 Dias Ltd. All rights reserved.
#   file: utils.py
#   mail: 2364939934@qq.com
#   date: 2020-07-02
#   describe:
# ================================================================
"""
: text_generate.py
: 2020-06-18
: fetch text from db text or any other source
    include mysql mongodb clickhouse text 
"""

import pdb
import pandas as pd
import pdb
import json
import re
import pickle
from bert_serving.client import BertClient
#import clickhouse_driver
#from clickhouse_driver import Client
import unittest
import pymongo
import pymysql
import traceback
#import redis
import threading
import queue
import json
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import sys
import datetime
from datetime import datetime

import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers


""" restore vec in mongo db 
    mongo save&restore vec 1d/2d
"""

ser_2d = lambda x:Binary(pickle.dumps(x, protocol=2))
dser_2d = lambda x:pickle.loads(x)
ser_1d = lambda x:x.tolist()
dser_1d = lambda x:np.fromiter(x)

# ======= 算法构建完毕，下面开始执行完整的构建词库流程 =======
# 语料生成器，并且初步预处理语料
# 这个生成器例子的具体含义不重要，只需要知道它就是逐句地把文本yield出来就行了

class EsHelper(object):
    ''' es 接口类 '''
    def __init__(self):
        host_list = [
            {"host":"172.20.0.104","port":9200},
        ]
        # create a es clint obj
        self.client = Elasticsearch("%s:%s"%(host_list[0]["host"], host_list[0]["port"]))

    def full_search(self, address, lat, lon, radius):
        """全文检索"""
        query = {
            "query": {
                "bool": {
                    # 影响相关度
                    "should":[
                        {"match": {"address": address }},
                        {"match": {"name": address }}
                    ],
                    # 不影响相关度
                    "must_not": [
                        {"match":{"city": "苏州市"}},
                        {"match":{"city": "天津市"}},
                        {"match":{"province": "河北省"}},
                        {"match":{"district": "丰台区"}},
                        {"match":{"district": "朝阳区"}}
                    ],
                    "filter": {
                        "geo_distance":{
                            "distance": radius,
                                "geohash":{
                                    "lat": lat,
                                    "lon": lon
                                }
                            }
                        }
                    }
                }
            }
        resp = self.client.search(index="mapapp", body=query, size=1)
        return resp

    def insert_one(self, client, actions):
        '''数据库中插入某个词条'''
        # actions.append(json.loads(line))
        try:
            helpers.parallel_bulk(client=client, thread_count=1, actions=actions)
            print(actions)
            return 0
        except:
            traceback.print_exc()
            return -1

    def init_index(self):

        doc = {
            'author': 'QinHaiNing',
            'text': 'Dias com.',
            'timestamp': datetime.now(),
        }

        #res = self.client.index(index="test-index", doc_type='address', id=1, body=doc)
        #res = es.get(index="address-baidu-index", doc_type='address', id=1)
        #print(res['_source'])
        self.client.indices.refresh(index="address-baidu-index")

    def search(self, text, size):
        print(text)
        res = self.client.search(
                index="address-baidu-index",
                doc_type="address",
                body = {
                    "query": {
                        "bool": {
                            "should": [
                                {"match": {"name": text["name"] }},
                                {"match": {"address": text["address"] }}
                            ],
                            "filter":
                                {"terms": {"tag": text["tag"] }}
                        }
                    }
                },
                size=size)
        #res = self.client.search(index="test-index", body={"query": {"match_all": {"%s"%text}}}, size=size)
        return res

    def timer(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            print('共耗时约 {:.2f} 秒'.format(time.time() - start))
            return res
        return wrapper

    @timer
    def gen(self, items):
        """ 使用生成器批量写入数据 """
        action = ({
            "_index": "address-baidu-index",
            "_type": "address",
            "_source": i
            } for i in items)
        helpers.bulk(self.client, action)


def _text_generator_():
    txts = glob.glob('/root/thuctc/THUCNews/*/*.txt')
    for txt in txts:
        d = codecs.open(txt, encoding='utf-8').read()
        d = d.replace(u'\u3000', ' ').strip()
        yield re.sub(u'[^\u4e00-\u9fa50-9a-zA-Z ]+', '\n', d)

class Progress:
    """显示进度，自己简单封装，比tqdm更可控一些
    iterator: 可迭代的对象；
    period: 显示进度的周期；
    steps: iterator可迭代的总步数，相当于len(iterator)
    """
    def __init__(self, iterator, period=1, steps=None, desc=None):
        self.iterator = iterator
        self.period = period
        if hasattr(iterator, '__len__'):
            self.steps = len(iterator)
        else:
            self.steps = steps
        self.desc = desc
        if self.steps:
            self._format_ = u'%s/%s passed' %('%s', self.steps)
        else:
            self._format_ = u'%s passed'
        if self.desc:
            self._format_ = self.desc + ' - ' + self._format_
        self.logger = logging.getLogger()
    def __iter__(self):
        for i, j in enumerate(self.iterator):
            if (i + 1) % self.period == 0:
                self.logger.info(self._format_ % (i+1))
            yield j

class StrMatch:
    def __init__(self):
        self.dct = {}
    def match(self, str1, str2):
        res = ""
        for i in range(len(str1)-1):
            val = self.dct.get(str1[i:i+2], 1)
            self.dct[str1[i:i+2]] = val
        for i in range(len(str2)-1):
            val = self.dct.get(str2[i:i+2], -1)
            if val>0:
                res+=str2[i:i+2]
            else:
                res+=","
        return res

def Q2Bs(sent):
    """全角转半角句子"""
    line = ""
    for char in sent:
        _c = Q2B(char)
        line+=_c
    return line

def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)

def clr(w):
    """ txt clr """
    if pd.isnull(w):
        return ""
    w = str(w)
    w.strip()
    w = re.sub("\.",",",w)
    w = re.sub("\r",",",w)
    w = re.sub("\n",",",w)
    w = re.sub("\t",",",w)
    return w

def levenshtein_distance(str1, str2, dv=1, av=1, mv=1):
    """
    计算字符串 str1 和 str2 的编辑距离
    :param str1
    :param str2
    :param av 增加惩罚
    :param dv 删除惩罚
    :param mv 修改惩罚
    :return:
    """
    matrix = [[ i + j for j in range(len(str2) + 1)] for i in range(len(str1) + 1)]
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            if(str1[i-1] == str2[j-1]):
                d = 0
            else:
                d = mv
            matrix[i][j] = min(matrix[i-1][j]+dv, matrix[i][j-1]+av, matrix[i-1][j-1]+d)
    #print(matrix[len(str1)][len(str2)])
    return matrix[len(str1)][len(str2)]

def short_left(sl, sr):
    if len(sl)>=len(sr):
        return sl, sr
    return sr, sl

def str_match(sl,sr):
    z = ""
    glt = 0
    if len(set(sl) & set(sr))==0:
        return []
    elif sl==sr:
        return [sl]

    q,p = short_left(sl, sr)

    i,j = 0,0
    #print(q,p)
    match_dct = set()
    _q = 0
    _p = 0
    for index_q, char_q in enumerate(q):
        for index_p, char_p in enumerate(p):
            if char_q == char_p:
                _ = 1
                while(True):
                    if p[index_p:index_p+_] in q and q[index_q:index_q+_] in p:
                        _+=1
                        continue
                    match_dct.add(p[index_p:index_p+_-1])
                    break
    long_match = set()
    for _ in list(match_dct):
        flag = True
        for __ in list(match_dct):
            if _ == __:
                continue
            elif _ in __:
                flag = False
                break
            else:
                pass
        if flag:
            long_match.add(_)
    return long_match

def load_address_txt(fname, sep, n):
    """ 加载文件名 """
    with open(fname, "r") as f:
        for line in f.readlines():
            try:
                yield line.split(sep)[n]
            except IndexError:
                print("ERROR: index error", line)

def load_address_reg(fname, cols):
    """ 加载文件名 """
    with open(fname, "r") as f:
        #resLst = []
        for line in f.readlines():
            res = []
            try:
                for col in cols:
                    res.append(re.findall("(?:%s\"\:\"(.*?)\")"%col, line)[0])
                yield res
            except IndexError:
                print("ERROR: index error", line)

def json_generator(fname):
    with open(fname, "r") as f:
        for line in f.readlines():
                if "pois" in line:
                    for item in json.loads(line[:-1])["pois"]:
                        try:
                          print(item["name"],"\t",item["name"],"\t",item["addr"])
                          yield item['name'], item['addr']
                        except KeyError:
                          continue
                else:
                    try:
                      dct = json.loads(line[:-1])
                      print(dct["name"],"\t",dct["name"],"\t",dct["address"])
                      yield dct["name"], dct["address"]
                    except KeyError:
                      continue

def text_generator(fname, sep, n):
    with open(fname, "r") as g:
        for line in g.readlines():
            try:
                yield Q2Bs(line.split(sep)[n])
            except IndexError:
                print("Error indexerror", line)
            except TypeError:
                print("Error typeerror", line)
            except:
                print("Error ", line)


def csv_generator(fname="thuc.cluster"):
    mDf = pd.read_csv(fname)
    for word in mDf["警情"]:
        yield Q2Bs(word)

def clr(w):
    """ txt clr """
    if pd.isnull(w):
        return ""
    w = str(w)
    w.strip()
    w = re.sub("\.",",",w)
    w = re.sub("\r",",",w)
    w = re.sub("\n",",",w)
    w = re.sub("\t",",",w)
    return w

def Q2B(uchar):
    """单个字符 全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e: #转完之后不是半角字符返回原来的字符
        return uchar
    return chr(inside_code)

def Q2Bs(sent):
    """全角转半角句子"""
    line = ""
    for char in sent:
        _c = Q2B(char)
        line+=_c
    return line

class RegularHelper(object):
    def __init__(self):
        pass
    def regular_extrace_address(self, text):
        results = []
        text = Q2Bs(text)
        results.extend(re.findall("(?:.*在)([^,]{3,})(?:\d*?\-\d*?)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,})(?:被)", text))
        results.extend(re.findall("(?:.*在)(.*?)(?:发现)", text))
        results.extend(re.findall("(?:.*在)(.*?)(?:门口)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}侧)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}站)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}路口)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}层)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}号)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}院)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}KTV)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}[东南西北]门)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}苑)", text))
        results.extend(re.findall("(?:.*在)([^,]{3,}旁)", text))
        results.extend(re.findall("(?:.*[报在:])([\u4e00-\u9fa5\dA-Za-z]{4,15}号[楼院]?)(?:,)?", text))
        results.extend(re.findall("(?:.*[报在:])([\u4e00-\u9fa5\dA-Za-z]{4,15}大[学厦])(?:,)?", text))
        results.extend(re.findall("(?:.*[报在:])([\u4e00-\u9fa5\dA-Za-z]{4,15}[楼堂馆所村屯庄镇])(?:,)?", text))
        results.extend(re.findall("(?:.*[报在:])([\u4e00-\u9fa5\dA-Za-z]{4,15}[楼堂馆所村屯庄镇])(?:[,被])?", text))
        res = [i for i in list(set(results)) if not '分钟' in i and not '月' in i and not '警' in i and not '手机' in i and len(i)>0]
        if len(res)>0:
            return  [sorted(res, key=lambda x:len(x), reverse=False)[0]]
        return []

class RedisHelper(object):
    """redis"""
    def __init__(self):
        self.r =redis.Redis(host="127.0.0.1",port=6379)

class MongoHelper(object):
    """mongo"""
    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        dblist = myclient.list_database_names()
        if "110" in dblist:
            print("db exists")
        self.mydb = myclient["110"]
        self.mycoll3 = self.mydb["base_data_3"]
        self.mycoll2 = self.mydb["base_data2"]
        self.mycoll = self.mydb["base_data"]
    #def __call__(self):
    #    return self.mycoll.find()

class Encoding(object):
    """txt 2 vec"""
    def __init__(self):
        self.server_ip = "127.0.0.1"
        #self.server_ip = "localhost"
        print('start conn Bert...')
        print(self.server_ip)
        self.bert_client = BertClient(ip="127.0.0.1")
        print('succ bert client')

    def encode(self, query):
        tensor = self.bert_client.encode(query)
        return tensor

    def query_similarity(self, query_list):
        tensors = self.bert_client.encode(query_list)
        return cosine_similarity(tensors)[0][1]

class MySQLHelper(object):
    ''' sample database 
        !!! do not release the code, cause it's password'''

    def __init__(self):
        db = pymysql.connect(
            host="39.98.169.101",
            user="haining",password="admin",
            database='SPD',
            charset="utf8")
        self.cursor = db.cursor()

    def __call__(self, cmd):
        res = self.cursor.execute(cmd)
        return self.cursor.fetchall()

class ClickHouseConn(object):
    def __init__(self):
        """ init clickhouse client"""
        clickhouse_user = 'name'
        clickhouse_pwd = 'pass'
        clickhouse_host_sq = '127.0.0.1'
        clickhouse_database = 'db'
        port = '9000'
        begin_time='2019-05-06'
        end_time='2019-05-12'

        mc = Client(host=clickhouse_host_sq, port=port)
        self.mc = mc

    def __call__(self, sql):
        """cmd run"""
        return self.mc.execute(sql)

class Test_Req(unittest.TestCase):
    """ test class """

    @classmethod
    def setUpClass(cls):
        print("run once before action")

    @classmethod
    def tearDownClass(cls):
        print("run once after action")

    def test_mysql_request_haidian(self):
        return 
        print("test_mysql_request_haidian(self)")
        mSQL = MySQLHelper()
        #res = mSQL("select * from haidian_sample_data_v1;")
        res = mSQL("show create table haidian_sample_data_v1;") #select * from haidian_sample_data_v1 limit 3;")
        print(res)
        #res = mSQL("select * from haidian_sample_data_v1 where classify_name='人力中介纠纷';")
        print(res)
        #res = mSQL("select JJDBH,BJNR from haidian_jiejing_data;")
        #res = mSQL("select JJDBH,BJNR from haidian_jiejing_data;")
        #res = mSQL("select JJDBH,BJNR from haidian_sample_data_v1;")
        f = open("sentimate-test-data","w+")
        """
        res = mSQL("select * from haidian_sample_data_v1;")
        lbs = set()
        for lin in res:
            if lin[3] == "人力中介纠纷":
                lbs.add(lin[1])
                f.write(lin[4].strip()+"\t1\n")
                print(lin[4])
        """
        #wds = "买东西 强迫 旅游 来京旅游 玉器 翡翠 文物 珠宝 貔貅 古玩 手镯 假币 红木 红木椅子 景泰蓝 家具 和氏璧 门票 费用 强制 纪念 纪念册 字画 椅子 葫芦 阿姨 小时工 景区 公园 旅行"
        wds = "劳务中介 找工作 聘 招工 求职 面试"
        f.write("\t".join("BJDH,BJNR".split(","))+"\n")
        for wd in wds.split(" "):
            print("select BJNR from haidian_jiejing_data where BJNR like '%"+wd+"%';")
            res = mSQL("select BJDH,BJNR from haidian_jiejing_data where BJNR like '%"+wd+"%';")
            for lin in res:
                if False: #lin[0] in lbs:
                    pass
                else:
                    #_lin = re.sub("[\r\n\t ]","",lin[0])
                    #f.write(_lin.strip()+"\t0\n")
                    print(lin)
                    try:
                        f.write("\t".join(list(lin))+"\n")
                    except:
                        continue
        print("mysql helper ok")

    def test_str_match(self, sl="1234567890000000000", sr="23456789000001231441"):
        str_match(sl,sr)

if __name__ == '__main__':
    unittest.main()

else:
    mEsHelper = EsHelper()
