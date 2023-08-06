#!encoding=utf-8

'''
rsa加密解密模块,确保信息安全

rsa 加密原理,两个大质数,容易求积,却不容易拆开,用其中一个做私钥,另一个做公钥
公钥用来加密,私钥用来解密

作者: 秦海宁
时间: 2021-03-19
联系: 2364839934@qq.com

'''

import rsa

# 对api的签名机制进行验证：签名用私钥,验签用公钥
class RsaEncrypt:

  def __init__(self, sign_str):
    self.sign_str = sign_str

  def rsa_generate(self):
    """
    生成私钥和公钥并保存
    :return:
    """
    pubkey, privkey = rsa.newkeys(1024) # 生成公钥和私钥
    pub = pubkey.save_pkcs1() # 保存公钥
    with open('public.pem', 'wb') as w_pub:
      w_pub.write(pub)
    pri = privkey.save_pkcs1() # 保存私钥
    with open('private.pem', 'wb') as w_pri:
      w_pri.write(pri)
    return "保存成功"

  @classmethod #类方法
  def read_rsa(self):
    """
    读取公钥和私钥
    :return:
    """
    with open('public.pem', 'rb') as publickfile:
      pub = publickfile.read()
      pubkey = rsa.PublicKey.load_pkcs1(pub)
    with open('private.pem', 'rb') as privatefile:
      priv = privatefile.read()
      # print(pub)
      privkey = rsa.PrivateKey.load_pkcs1(priv)
    return pubkey, privkey

  def str_sign(self):
    privkey = self.read_rsa()[1] # 先将要加密的数据转成二进制
    str_encode = self.sign_str.encode() # 用私钥进行加密,并设置加密算法
    signature = rsa.sign(str_encode, privkey, 'SHA-256') # 签名加密算法可以更换比如：SHA-256
    # print(signature)
    return signature

  def sign_verify(self, signature):
    """
    验证签名是否正确,如果正确,则返回签名算法,否则返回验证失败
    :param signature:
    :return:
    """
    pubkey = self.read_rsa()[0]
    try:
      agl = rsa.verify(self.sign_str.encode(), signature, pubkey)
      # print(type(agl))
      print(agl) # 返回加密算法代表验签成功
      return True
    except rsa.VerificationError:
      print("验证失败")
      return False

# 对数据进行加密:加密用公钥,解密用私钥
class DataEncrypt:

  def __init__(self, data_str):
    self.data_str = data_str
    self.secret_key = RsaEncrypt.read_rsa()# 调用RsaEncrypt类的读取密钥对方法

  def data_encrypt(self):
    """
    用公钥对数据进行加密
    :return:
    """
    str_encrypt = rsa.encrypt(self.data_str.encode(), self.secret_key[0])
    print(str_encrypt) # 加密后看着像二进制,但有不太像,看不懂
    return str_encrypt

  def data_decrypt(self, encrypt):
      '''
      使用私钥对数据进行解密
      '''
      str = rsa.decrypt(encrypt, self.secret_key[1]).decode()
      print(str) # 返回加密前的数据
      return str

if __name__ == '__main__':
  # 验证签名机制
  input_txt = 'ivystar'
  sing_test = RsaEncrypt(input_txt)
  # sing_test.rsa_generate() # 生成密钥会覆盖当前密钥，请注意存档
  sing_test.sign_verify(sing_test.str_sign())

  # 验证加密解密机制
  data = DataEncrypt(input_txt)
  result = data.data_decrypt(data.data_encrypt())
  try:
      assert result == input_txt
      print("密码正确")
  except AssertException:
      print("密码错误")

