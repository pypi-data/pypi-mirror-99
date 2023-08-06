#!encoding=utf-8
"""
html内容解析
"""
import sys
import requests_html
from requests_html import HTMLSession
import re
import pdb

class HttpAnalyze(object):
    '''
    http 访问结果解析
    '''
    def __init__(self):
        print('init HttpAnalyze')
        session = HTMLSession()
        self.session = session

    def get_url(self, url):
        '''
        读取url内容
        '''
        res = self.session.get(url)
        return res

    def text_filter(self, res):
        '''
        过滤出带有汉字的句子
        '''
        texts_a = [i.strip() for i in res.html.full_text.split(u"\n") if len(i.strip())>0 and re.search("^[\u4e00-\u9fa5]", i.strip())]
        texts_b = [i.strip() for i in res.html.text.split(u"\n") if len(i.strip())>0 and re.search("^[\u4e00-\u9fa5]", i.strip())]
        texts_c = list(set(texts_a + texts_b))
        return texts_c

    def links_filter(self, res):
        '''
        返回所有的链接
        '''
        target_links = []
        links = list(res.html.links) + list(res.html.absolute_links)
        for _ in links:
            if _[:4] == "http":
                target_links.append(_)
            else:
                target_links.append(res.html.url[:-1]+_)
        return list(set(target_links))

    def __call__(self, url):
        content = self.get_url(url)
        texts = self.text_filter(content)
        links = self.links_filter(content)
        page_info = {}
        page_info["texts"] = texts
        page_info["links"] = links
        page_info["url"] = url
        return page_info

if __name__ == "__main__":
    ha = HttpAnalyze()
    response = ha("http://www.triplet.com.cn")
    print(response)
