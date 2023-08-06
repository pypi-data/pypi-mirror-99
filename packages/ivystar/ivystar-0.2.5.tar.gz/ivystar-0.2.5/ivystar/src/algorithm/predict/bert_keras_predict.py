#!encoding=utf-8

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
import numpy as np
import sys
sys.path.append("/app/ivystar")
from ivystar.src.conf import BERT_MODEL_PATH
from ivystar.src.algorithm.predict.base_predict import BasePredictClass
from ivystar.src.algorithm.similar.calculate_similarity import pearson
print("BERT_MODEL_PATH", BERT_MODEL_PATH)
import os

#BERT_MODEL_PATH = "/home/qin/release/model/chinese_L-12_H-768_A-12"

'''
加载google预言模型，完成语言向量化
'''

class Word2VecPredict(BasePredictClass):
    def __init__(self, name):
        BasePredictClass.__init__(self, name)
        config_path = os.path.join(BERT_MODEL_PATH, "bert_config.json")
        checkpoint_path = os.path.join(BERT_MODEL_PATH, "bert_model.ckpt")
        dict_path = os.path.join(BERT_MODEL_PATH, "vocab.txt")

        self.kvs = {}
        self.kvs["config_path"] = config_path
        self.kvs["checkpoint_path"] = checkpoint_path
        self.kvs["dict_path"] = dict_path

    def load_model(self):
        tokenizer = Tokenizer(self.kvs["dict_path"], do_lower_case=True)  # 建立分词器
        model = build_transformer_model(self.kvs["config_path"], self.kvs["checkpoint_path"])  # 建立模型，加载权重
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, texts, lenth=512, size=10):
        '''
        # 编码测试
        texts 等转换的文本
        lenth 每个句子保留多少个字符
        size 保留多少个句子
        '''
        texts = BasePredictClass.row_col_pendding(texts, lenth, size)
        token_ids_array, segment_ids_array = [], []
        for text in texts:
            token_ids, segment_ids = self.tokenizer.encode(text)
            token_ids_array.append(token_ids)
            segment_ids_array.append(segment_ids)
        res = self.model.predict([np.array(token_ids_array), np.array(segment_ids_array)])
        print(texts)
        print(res)
        return res

if __name__ == "__main__":
    mModel = Word2VecPredict("word2vec")
    mModel.load_model()
    res = mModel.predict(["中国" for i in range(1024)])

