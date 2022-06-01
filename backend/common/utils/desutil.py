# des模式  填充方式  ECB加密方式
import base64
from pyDes import *  # pip install pyDes


class DEncry:
    def __init__(self, Des_Key='12345678', Des_IV='abcdefgh'):
        self.Des_Key = Des_Key  # Key
        self.Des_IV = Des_IV  # 自定IV向量

    # 使用DES加base64的形式加密
    def encrypt(self, s):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(s)
        # EncryptStr = binascii.unhexlify(k.encrypt(str))
        return base64.b64encode(EncryptStr).decode()  # 转base64编码返回

    # des解码
    def decrypt(self, s):
        s = base64.b64decode(s)
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        DecryptStr = k.decrypt(s, padmode=PAD_PKCS5)
        return DecryptStr.decode()


if __name__ == "__main__":
    de = DEncry()
    passwd = de.encrypt("Fxs2020@Fxs2020@Fxs2020@")
    print("passwd: %s" % passwd)
    ret = de.decrypt(passwd)
    print("result: %s" % ret)
