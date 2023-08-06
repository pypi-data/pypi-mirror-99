#!encoding=utf-8

class BasePredictClass(object):
    '''
    预测基类
    '''
    def __init__(self, name=""):
        self.name = name

    def load_model(self, **kws):
        pass

    def predict(self, texts, lenth, size):
        pass

    @staticmethod
    def row_col_pendding(texts, lenth, size):
        '''控制句子长度，句子数量'''
        return [text[:lenth] for text in texts][:size]


