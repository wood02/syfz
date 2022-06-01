#!/usr/bin/python3
# coding:utf-8


# 根据机器码生成激活码，并进行对应的加密解密
import json
import platform
import subprocess
from datetime import datetime, timedelta

from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
# from wmi import WMI
import base64
from subprocess import Popen, PIPE
import os, sys

from Syfz.settings import BASE_DIR


class ActivationCode(object):

    def __init__(self):
        pass

    def generate(self, machine_code: str, valid_period: int, activation_module: list):
        """
              初始化
              :param machine_code: 机器码
              :param valid_period: 有效期,单位为天
              :param activation_module: 要激活的模块
              """
        encrypt_activation_code = ""
        encrypt_dict = {"machine_code": "", "activation_module": activation_module, "expire_date": ""}
        # 根据有效期算出过期日期
        current_date = datetime.now()
        expire_date = current_date + timedelta(days=valid_period)
        expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
        # 添加机器码
        encrypt_dict["machine_code"] = machine_code
        # 添加过期时间
        encrypt_dict["expire_date"] = expire_date
        # print(json.dumps(encrypt_dict))
        encrypt_activation_code = self.encrypt(json.dumps(encrypt_dict))
        # encrypt_activation_code =self.encrypt("aaaaa")xxxxx
        # print(encrypt_activation_code)
        # aaa = encrypt_activation_code.decode('utf8')
        # print("返回激活码：",aaa)
        return encrypt_activation_code

    def encrypt(self, raw):
        """
        加密
        :param raw: 待加密字符串
        :return: 加密过后的字符串
        """
        ras_obj = RSAUtil()
        return ras_obj.encrypt_data(raw)

    def decrypt(self, enc):
        """
        解密
        :param enc: 加密字符串
        :return: 解密过后的字符串
        """
        ras_obj = RSAUtil()
        return ras_obj.decrypt_data(enc)


class AESUtil(object):

    def __init__(self):
        self.key = "asjkfasdsfhskljf".encode("utf8")

    def decode_base64(self, data):
        """
        对要加密的数据进行处理
        :param data: 要加密的数据(str)
        :return: 处理过后的数据(bytes)
        """
        # 因为传过来的加密可能会是str类型，要进行类型转换
        if not isinstance(data, bytes):
            data = bytes(data, encoding="utf8")
        # 有可能处理密文时候会报错：'Error: Incorrect padding'
        # 这是因为密文长度不符合规格，对base64解码的string补齐等号就可以了,明文长度要为16或者十六的倍数
        # 下面就是处理方法
        missing_padding = 16 - len(data) % 16
        if missing_padding:
            data += b'=' * missing_padding
        return data

    def encrypt(self, raw):
        """
        加密
        :param raw: 待加密的数据
        :return: 加密过后的数据
        """
        raw = self.decode_base64(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        raw_bytes = cipher.encrypt(raw)
        raw_str = self.bytes_to_str(raw_bytes)
        return raw_str

    def decrypt(self, enc):
        """
        解密
        :param enc: 加密数据
        :return: 解密过后的数据
        """
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, self.key)
        return cipher.decrypt(enc)

    def bytes_to_str(self, bytes_data):
        """
        bytes转str
        :param bytes_data: 要转换的字节对象
        :return: 转换过后的字符串
        """
        # result = str(bytes_data, encoding="utf8")
        result = str(base64.b64encode(bytes_data), encoding='utf-8')
        return result


class RSAUtil(object):
    def __init__(self):
        self.private_key_path = os.path.join(BASE_DIR, 'common/utils/private_key/rsa_private_key.pem')
        self.public_key_path = os.path.join(BASE_DIR, 'common/utils/public_key/rsa_public_key.pem')

    def generate_key(self):
        """
        生成公钥和私钥，公钥私钥必须由同一个对象生成
        :return: 公钥和私钥存放路径
        """
        random_generator = Random.new().read
        rsa = RSA.generate(2048, random_generator)
        private_key = rsa.exportKey()
        # print(private_key.decode('utf-8'))

        with open(self.private_key_path, 'wb')as f:
            f.write(private_key)
        public_key = rsa.publickey().exportKey()
        # print(public_key.decode('utf-8'))
        with open(self.private_key_path, 'wb')as f:
            f.write(public_key)

    def get_key(self, key_file):
        with open(key_file) as f:
            data = f.read()
            key = RSA.importKey(data)

        return key

    def encrypt_data(self, msg, length=200):
        # 单次加密串的长度最大为 (key_size/8)-11
        # 1024bit的证书用100， 2048bit的证书用 200
        private_key = self.get_key(self.public_key_path)
        msg = base64.b64encode(msg.encode("utf-8")).decode('utf8')
        cipher = PKCS1_cipher.new(private_key)
        res = []
        for i in range(0, len(msg), length):
            res.append(cipher.encrypt(msg[i:i + length].encode('utf8')))
        result = base64.b64encode(b"".join(res)).decode('utf8')
        # result = b"".join(res)
        # print(result)
        return result

    def decrypt_data(self, encrypt_msg, default_length=256):
        # 私钥解密
        private_key = self.get_key(self.private_key_path)
        # 传进来的是str需要改变bytes
        msg = base64.b64decode(encrypt_msg)
        length = len(msg)
        # default_length = 256
        error_msg = "解密错误".encode("utf8")
        priobj = PKCS1_cipher.new(private_key)
        # 长度不用分段
        if length < default_length:
            return b''.join(priobj.decrypt(msg, error_msg))
        # 需要分段
        offset = 0
        res = []
        while length - offset > 0:
            if length - offset > default_length:
                res.append(priobj.decrypt(msg[offset:offset + default_length], error_msg))
            else:
                res.append(priobj.decrypt(msg[offset:], error_msg))
            offset += default_length
            m = b''.join(res)
            n = m.decode("utf-8")
        return base64.b64decode(n).decode('utf-8')

    def check(self):
        msg = "{'app_id':1, 'unid_id':'232323232', 'app_name':'小白'}"
        print("原字符串", msg)
        encrypt_text = self.encrypt_data(msg)
        print('加密过后的字符串', encrypt_text)
        # decrypt_text = self.decrypt_data(encrypt_text)
        decrypt_text = self.decrypt_data(encrypt_text)
        print('解密过后的字符串', decrypt_text)
        print(msg == decrypt_text)


def get_machine_code():
    os_type = platform.system()
    lines = []
    if os_type == "Windows":
        from wmi import WMI
        c = WMI()
        # for physical_disk in c.Win32_DiskDrive():
        n = c.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip()
        lines.append({"Serial Number": n})
    else:
        p = subprocess.Popen(["dmidecode | grep Serial"], shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data = p.stdout

        while True:
            line = str(data.readline(), encoding="utf-8")
            if line == '\n':
                break
            if line:
                d = dict([line.strip().split(': ')])
                lines.append(d)
            else:
                break
        # [{'Serial Number': 'e8a19782-57ed-4276-afcb-38ba75b7327a'}, {'Serial Number': 'Not Specified'}, {'Serial Number': 'Not Specified'}, {'Serial Number': 'Not Specified'}]
    return lines

    # def test_sign():
    #     msg = 'coolpython.net'
    #     sign = rsa_private_sign(msg)
    #     print(rsa_public_check_sign(msg, sign))


if __name__ == '__main__':
    testdata = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA0BUcETbJnfDaepDIIMNj
HPlYeeWSKShw5qxohEkp52dMSEEjsEYeOfnooc4N9l9f5B7fY5IHovSYxUmLLOO4
GhYijXWhXrE3+NUaEAT99/eU5PikOVtOQYRfUXT+lvQ5t1ExBOTyXZXntVKj/kCB
PA9olaA0hAKmWK4fB7yWrgjqv4ICB5tiHhLixoF7MGmhgdfwsXtOL3RgkOyyfYzk
7Y0VKJ64ULXHoorbkXYpoVNmnaiViYOk5bsMiIqlgoKLpjqOmW//MMp7uwrvycHF
0Nj2jsJCr2m6kUiPkNAHtvJAXkuDMI/HUkcDHXtx/otothTwT5dXs0iFT22rW67q
+QIDAQAB
-----END PUBLIC KEY-----"""
    # aesutil = AESUtil()
    # aesutil.decode_base64(testdata)
    # aa = aesutil.encrypt(testdata)
    # print(aa)
    # bb = aesutil.decrypt(aa)
    # print(bb)
    # r = RSAUtil()index.blade.php
    # r.generate_key()
    # r.generate_public_key()
    # r.check()

    # a = ActivationCode('e8a19782-57ed-4276-afcb-38ba75b7327a', 90, [0, 1, 2])
    # a = ActivationCode()
    # b = a.generate('SD0L02320L1TH6510CS8', 0, [0, 1, 2])
    # print( b)
    # c = a.decrypt(b)
    # print(c)

    d = get_machine_code()
    print(d)
