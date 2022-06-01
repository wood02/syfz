import json
import logging
import random
from hashlib import md5


def make_response(data=None, message='success', code=200):
    resp = dict()
    resp['message'] = message
    resp['code'] = code
    resp['data'] = data
    if code == 200:
        resp['success'] = True
    else:
        resp['success'] = False

    return resp


def safe_json_load(json_data):
    try:
        if not json_data:
            return None
        return json.loads(json_data)
    except Exception as e:
        logging.error("%s, data: %s" % (e, json_data))
        return None


def get_object_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return []


def getRandomStr(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    characters = random.sample(alphabet, num)
    return ''.join(characters)


def create_salt(length=4):
    """获取由4位随机大小写字母、数字组成的salt值"""
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    for index in range(length):
        salt += chars[random.randint(0, len_chars)]
    return salt


def create_md5(pwd, salt):
    """获取原始密码+salt的md5值"""
    md5_obj = md5()
    pwd = pwd.encode('utf-8')
    salt = salt.encode('utf-8')
    md5_obj.update(pwd + salt)
    return md5_obj.hexdigest()


if __name__ == '__main__':
    pass
