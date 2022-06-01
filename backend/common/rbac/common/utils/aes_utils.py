import base64

from Crypto.Cipher import AES
from Crypto.SelfTest.st_common import a2b_hex, b2a_hex


class AESUtil(object):

    def __init__(self):
        self.key = "asjkfasdsfhskljf".encode("utf8")

    def encrypt(self, data):
        """
        加密
        :param raw: 待加密的数据
        :return: 加密过后的数据
        """

        BLOCK_SIZE = 16  # Bytes
        # 数据进行 PKCS5Padding 的填充
        pad = lambda s: (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))
        raw = pad(str(data))
        # 通过key值，使用ECB模式进行加密
        cipher = AES.new(self.key, AES.MODE_ECB)
        # 得到加密后的字节码
        encrypted_text = cipher.encrypt(bytes(raw, encoding='utf-8'))
        # 字节码转换成十六进制  再转成 字符串
        encrypted_text_hex = str(b2a_hex(encrypted_text), encoding='utf-8')
        return encrypted_text_hex

    def decrypt(self, encrypted_text_hex):
        """
        解密
        :param enc: 加密数据
        :return: 解密过后的数据
        """
        # 去掉 PKCS5Padding 的填充
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        # 通过 key 值进行
        cipher = AES.new(self.key, AES.MODE_ECB)
        data_response = unpad(cipher.decrypt(a2b_hex(encrypted_text_hex))).decode('utf8')
        return data_response

