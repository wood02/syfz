import json

import requests


class RequestAPi(object):
    """
    请求api的类
    """
    # headers = {"Authorization": "JWT xxx", "Content-Type": "application/json"}
    def __init__(self,url,header=None,param=None,request_type='get'):
        self.url = url
        self.header = header
        self.param = param
        self.request_type = request_type

    def get_api(self):
        kg = {}
        kg["url"] = self.url
        if self.param is not None:
            kg["params"] = self.param
        if self.header is not None:
            kg["headers"] = self.header
        try:
            response = requests.get(**kg)
            if response.status_code == 200:
                return {'status': 1, 'data': response.text}
            else:
                return {'status': 0, 'data': '接口请求失败'}
        except Exception as e:
            return {'status': 0, 'data': '接口请求失败,错误原因:{}'.format(e)}

    def post_api(self):
        kg = {}
        kg['url'] = self.url
        if self.param is not None:
            kg["data"] = json.dumps(self.param)
        if self.header is not None:
            kg["headers"] = self.header
        try:
            response = requests.post(**kg)
            if response.status_code == 200:
                return {'status': 1, 'data': response.text}
            else:
                return {'status': 0, 'data': '接口请求失败'}

        except Exception as e:
            return {'status': 0, 'data': '接口请求失败,错误原因:{}'.format(e)}



class UserAPi(object):
    def __init__(self,uname,pwd):
        self.uname = uname
        self.pwd = pwd

    def get_login_api(self):
        api_obj = RequestAPi(url='http://47.105.166.143:8811/api/user/login_without_token/')
        api_obj.param = {'username':self.uname,'password':self.pwd}
        api_obj.header = {'content-type': 'application/json'}
        response = api_obj.post_api()
        return response

    def get_token(self):
        token = ''
        req = self.get_login_api()
        if req['status']:
            try:
                api_data = json.loads(req['data'])
                if api_data['code']==200:
                    token= api_data['data']['token']
            except Exception as e:
                print(e)
        return token


class BlockIpApi(object):
    def __init__(self, ip, token):
        self.ip = ip
        self.token = token

    def get_blockiplist(self):
        api_obj = RequestAPi(url='http://47.105.166.143:8811/api/firewall/blockiplist/')
        api_obj.param = {'ip': self.ip}
        api_obj.header = {'content-type': 'application/json', 'authorization': 'JWT '+self.token}
        response = api_obj.get_api()
        print(response)
        return response

if __name__ == '__main__':
    # a = UserAPi('hwtools','hwtools123480')
    # token = a.get_token()
    # print(token)
    token ="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Imh3dG9vbHMiLCJleHAiOjE2MjgyMTg0NDIsImVtYWlsIjoiIn0.D_klVoHS8Z4AnC8LRym2PHqUcoGJt-WCnet1DV5wa-c"
    b = BlockIpApi('127.0.0.1',token)
    b.get_blockiplist()