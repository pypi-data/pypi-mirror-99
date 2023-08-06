#!encoding=utf-8

from bert4keras.models import build_transformer_model
from bert4keras.tokenizers import Tokenizer
import numpy as np
from ivystar.src.conf import BERT_MODEL_PATH

config_path = os.path.join(BERT_MODEL_PATH, "bert_config.json")
checkpoint_path = os.path.join(BERT_MODEL_PATH, "bert_model.ckpt")
dict_path = os.path.join(BERT_MODEL_PATH, "vocab.txt")

tokenizer = Tokenizer(dict_path, do_lower_case=True)  # 建立分词器
model = build_transformer_model(config_path, checkpoint_path)  # 建立模型，加载权重

# 编码测试
token_ids, segment_ids = tokenizer.encode(u'语言模型')

print('\n ===== predicting =====\n')
print(model.predict([np.array([token_ids]), np.array([segment_ids])]))
