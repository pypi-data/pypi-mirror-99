#encoding=utf-8
# ================================================================
#   Copyright (C) 2020 ivystar Ltd. All rights reserved.
#   file: utils.py
#   mail: 2364939934@qq.com
#   date: 2020-07-02
#   describe: interface for mongodb
# ================================================================

from ivystar.src.dataio.base_helper import DataBaseHelper
import pymongo
from ivystar.src.conf import MONGO_IP
from ivystar.src.conf import MONGO_PORT

class MongoHelper(DataBaseHelper):
    """mongo client"""
    def __init__(self, ip, port):
        DataBaseHelper.__init__(self)
        myclient = pymongo.MongoClient("mongodb://%s:%s/"%(ip, port))
        for db in myclient.list_database_names():
            for coll in myclient[db].list_collection_names():
                print("%s.%s"%(db, coll))
        self.cli = myclient

if __name__ == "__main__":
    mh = MongoHelper(MONGO_IP, MONGO_PORT)
