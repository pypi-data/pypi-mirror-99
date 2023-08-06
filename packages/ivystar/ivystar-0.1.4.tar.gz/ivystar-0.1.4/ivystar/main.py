#!encoding=utf-8
'''
将通用接口封装为pkg，方便调用

主要包括:
dataio 数据接口
algorithm 算法工具
web 网络接口
utils 工具
conf 配置

作者:秦海宁
时间: 2021-03-19
联系方式: 2364839934@qq.com

'''

from src.utils.rsa_utils import RsaEncrypt

class IvyStar(object):
    def __init__(self):
        self.signature()

    def signature(self):
        '''
        rsa解密后，可以使用功能
        '''
        try:
            input_txt = 'ivystar'
            sing_test = RsaEncrypt(input_txt)
            if sing_test.sign_verify(sing_test.str_sign()):
                print("解密成功，全部功能解锁")
                return True
            else:
                print("请联系管理员获得密钥,您的行为将被记录.")
        except FileNotFoundError:
            print("请联系管理员获得密钥,您的行为将被记录.")

if __name__ == "__main__":
    ist = IvyStar()

