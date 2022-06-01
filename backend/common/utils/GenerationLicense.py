#!/usr/bin/python3
# coding:utf-8


import base64
import json
import os
from datetime import datetime, timedelta
from random import sample
from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.SelfTest.st_common import b2a_hex, a2b_hex
from Crypto.Signature import PKCS1_v1_5

from Syfz.settings import BASE_DIR


class LicenseServer(object):
    """
    服务端，用来生成激活码
    """

    def __init__(self, machine_code: str, valid_period: int, activation_module: list):
        """
        初始化
        :param machine_code: 机器码
        :param valid_period: 有效期，单位为天
        :param activation_module: 需要激活的模块（编号）
        """
        self.machine_code = machine_code
        self.valid_period = valid_period
        self.activation_module = activation_module
        self.private_key_path = os.path.join(BASE_DIR, 'common/utils/private_key/rsa_private_key.pem')

    def generation_aes_key(self):
        """
        生成一个16位的随机数为aes_key
        :return: aes_key
        """

        return "".join(sample('abcdefghijklmnopqrstuvwxyz1234567890', 16))

    def generation_license(self):
        """
        生成激活码
        :return: 激活码
        """
        # License = AesKey16 + AesEnc(data).length + AesEnc(data) + RsaSign(AesEnc(data));
        # 获取AesKey
        aes_key = self.generation_aes_key()
        # 处理授权信息
        authorization_info = self.deal_with_info()
        # 加密授权信息
        enc_info = self.aes_encrypt(authorization_info, aes_key)
        enc_info_len = hex(len(enc_info))[2::].rjust(4, '0')  # 授权信息的长度(16进制去掉0x，左端补0，得到一个四位数的字符串)
        # rsa签名
        res_sign = self.rsa_sign(enc_info)
        license = aes_key + enc_info_len + enc_info + res_sign
        return license

    def deal_with_info(self):
        """
        处理授权信息
        :return:
        """
        encrypt_dict = {"machine_code": "", "activation_module": self.activation_module, "expire_date": ""}
        # 根据有效期算出到期时间
        current_date = datetime.now()
        expire_date = current_date + timedelta(days=self.valid_period)
        expire_date = expire_date.strftime("%Y-%m-%d %H:%M:%S")
        # 添加机器码
        encrypt_dict["machine_code"] = self.machine_code
        # 添加到期时间
        encrypt_dict["expire_date"] = expire_date
        return json.dumps(encrypt_dict)

    def rsa_sign(self, data):
        """
        生成rsa_sign签名
        :param data: 待签名的数据
        :return:
        """
        try:
            private_key = self.get_key(self.private_key_path)
            signer = PKCS1_v1_5.new(private_key)
            hash_obj = MD5.new(data.encode('utf-8'))
            signature = base64.b64encode(signer.sign(hash_obj))
            return signature.decode('utf-8')
        except FileNotFoundError:
            print("私钥路径不存在，请修改路径！")
            return None

    def get_key(self, key_file):
        with open(key_file) as f:
            data = f.read()
            key = RSA.importKey(data)

        return key

    def aes_encrypt(self, data, key):
        """
        对授权信息进行aes加密
        :param data: 待加密的字符串
        :param key: Aes密钥
        :return: 加密过后的授权信息
        """
        # 处理待加密的字符串
        BLOCK_SIZE = 16  # Bytes
        # 数据进行 PKCS5Padding 的填充
        pad = lambda s: (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))
        raw = pad(str(data))
        # 通过key值，使用ECB模式进行加密
        cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        # 得到加密后的字节码
        encrypted_text = cipher.encrypt(bytes(raw, encoding='utf-8'))
        # 字节码转换成十六进制  再转成 字符串
        encrypted_text_hex = str(b2a_hex(encrypted_text), encoding='utf-8')
        return encrypted_text_hex


class LicenseClient(object):
    """
    客户端，用来验证激活码
    """

    def __init__(self, license):
        self.license = license
        self.public_key_path = os.path.join(BASE_DIR, 'common/utils/public_key/rsa_public_key.pem')

    def check_license(self):
        """
        校验激活码
        :return: 校验结果
        """
        # 校验签名
        result = self.deal_with_license()
        return result

    def deal_with_license(self):
        """
        处理激活码
        :return: 校验结果
        """
        aes_key = self.license[0:16].encode('utf-8')  # 16位aes密钥
        info_len = int(self.license[16:20], 16)  # 加密信息长度
        enc_info = self.license[20:20 + info_len]  # 加密信息
        # 需要验证签名过后才能解密信息
        signature = self.license[20 + info_len::]
        verify_result = self.verify_sign(signature, enc_info)

        if verify_result:
            dec_info = self.aes_decrypt(aes_key, enc_info)  # 解密过后的信息
            return dec_info
        else:
            return {"code": 0, "message": "签名校验失败", "data": None}

    def aes_decrypt(self, key, encrypted_text_hex):
        """
        aes解密
        :param key: aes密钥(byte类型)
        :param encrypted_text_hex: 待解密的字符串
        :return:
        """
        # 去掉 PKCS5Padding 的填充
        unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        # 通过 key 值进行
        cipher = AES.new(key, AES.MODE_ECB)
        data_response = unpad(cipher.decrypt(a2b_hex(encrypted_text_hex))).decode('utf8')
        return data_response

    def verify_sign(self, signature, enc_data):
        """

        :param signature: 签名
        :param enc_data: 要验证的部分
        :return: 签名是否正确（bool类型）
        """
        try:
            public_key = self.get_key(self.public_key_path)
            verifier = PKCS1_v1_5.new(public_key)
            hash_obj = MD5.new(enc_data.encode('utf-8'))
            return verifier.verify(hash_obj, base64.b64decode(signature))
        except FileNotFoundError:
            print("私钥路径不存在，请修改路径！")
            return None

    def get_key(self, key_file):
        with open(key_file) as f:
            data = f.read()
            key = RSA.importKey(data)
        return key


if __name__ == '__main__':
    machine_code = "BP1G8FIMXB617K8RDG6F"
    activation_module = ["MGXXJC"]
    valid_period = 90
    s = LicenseServer(machine_code, valid_period, activation_module)
    license = s.generation_license()
    print(license)
    #     license = """2bjoclwe5dkz4r3a012075fb5375316bc9206640dbe6a7714bff0aed196c5c8325b269ae9f46afe0efef3106a112f5395445f2e351f17b5c9f13ad4c65a761535c1bf349fa0f768c64770cfd35d23d56d3699b301f1df6b278fba4b8715327bd5b38da08e21aa1cb5aeedaa5d4005892f182b10db52f56289fb8cfb5b691f61564d55f80ec3bc38792dec4079f90606e0f3e8a96870b415b1a5dFzyX/WUJ0+vWuti3wTgsCVpAgpl9aV7A/ffRZQnNnoDTrwD37RV+Tcy+quQv86FBeSjhJ0N6NJHQ5+QW32XyGRtMsKZmetMMkrc+NtavWX9vgcNtRAcYajCnmSMoKH663mzgMzdKyS+Vi5ixbirEP2dP4ozKNPR/OrO/Apt+7q8OpOEZTm00vP5mjkRfWrlyJD7ymfB89sOcwUhzaJ43u9LXp4liJRMqOHb2cZPR/Pi8d2pktJw7cOxCo8909Ufh5M5ZdWDkixtwdmjkC7tmOthi/MiipB6GX2npQWkjw8LCvfSK6eoESh+dqE9CYBQHqUO2u9+HBHOwiEnhKDnH+w==
    # """
    c = LicenseClient(license)
    print(c.check_license())
