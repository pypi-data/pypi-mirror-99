#!encoding=utf-8

# 将路径配置入环境变量

import os

PROJECT_PATH = os.environ.get("PROJECT_PATH", "")
SIGNATURE_FILE_PATH = os.environ.get("SIGNATURE_FILE_PATH", "")
BERT_MODEL_PATH = os.environ.get("BERT_MODEL_PATH", "")

# 'bert/chinese_L-12_H-768_A-12/bert_config.json'
