#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tenacity import retry, stop_after_attempt, wait_random

from Syfz.setup import django_setup
import base64
import datetime
import json
import requests

from apps.alarm.models import FofaToken, Attack
from apps.system.models import GlobalConfig
from common.current.log import get_logger
from common.utils.desutil import DEncry
from common.utils.md5 import md5


class FofaClient:
    def __init__(self):
        self.des = DEncry()
        self.tokens = self.get_toekns()
        v = GlobalConfig.objects.filter(key="FOFA_URLS").first().value
        self.base_url = v["base_url"]['url']
        # self.base_url = "https://fofa.info"
        self.search_api_url = "/api/v1/search/all"
        self.login_api_url = "/api/v1/info/my"
        self.stats_api_url = "/api/v1/search/stats"

        self.get_logger = get_logger("utils", 'fofa.log', filter=lambda record: "fofa" in record["extra"])
        self.logger = self.get_logger.bind(fofa=True)
        # self.get_userinfo()  # check email and key

    def get_userinfo(self):
        api_full_url = "%s%s" % (self.base_url, self.login_api_url)
        for token in self.tokens:
            email = self.des.decrypt(token.email)
            key = self.des.decrypt(token.key)
            param = {"email": email, "key": key}
            res = self.__http_get(api_full_url, param)
            # print(api_full_url)
            # print(res.text)
            return res.json()

    @retry(stop=stop_after_attempt(5), wait=wait_random(min=1, max=5))
    def __http_get(self, url, param):
        try:
            response = requests.get(url=url, params=param, timeout=10)
        except Exception as e:
            self.logger.error(f"Fofa错误: {str(e)}")
            raise Exception("连接错误！")
        else:
            return response

    def get_stats(self, query_str):
        """
        企业会员
        :param query_str:
        :return:
        """
        # 转成bytes string
        bytes_str = query_str.encode(encoding="utf-8")

        # base64 编码
        encode_str = base64.b64encode(bytes_str)
        qbase64 = encode_str.decode()

        api_full_url = "%s%s" % (self.base_url, self.stats_api_url)
        for token in self.tokens:
            email = self.des.decrypt(token.email)
            key = self.des.decrypt(token.key)
            param = {"qbase64": qbase64, "email": email, "key": key}
            res = self.__http_get(api_full_url, param)
            # print(api_full_url)
            # print(res.text)
            return res.json()

    def get_json_data(self, query_str, page=1, size=25, fields="", full=True):
        api_full_url = "%s%s" % (self.base_url, self.search_api_url)
        # 转成bytes string
        bytes_str = query_str.encode(encoding="utf-8")

        # base64 编码
        encode_str = base64.b64encode(bytes_str)
        qbase64 = encode_str.decode()
        errmsg = ""
        for token in self.tokens:
            email = self.des.decrypt(token.email)
            key = self.des.decrypt(token.key)
            param = {"qbase64": qbase64, "email": email, "key": key, "page": page, "size": size,
                     "full": full, "fields": fields}
            res = self.__http_get(api_full_url, param)
            # self.logger.info(f"Fofa token信息: {res.text}")
            if res.status_code == 200:
                res = res.json()

                res['qbase64'] = qbase64

                res['error'] = res.get('errror', res.get('error', True))
                if res['error']:
                    self.logger.error(f"Fofa错误信息:{token.id} {res['errmsg']}")
                    token.status = 2
                    token.error_num = token.error_num + 1
                    token.error_msg = res['errmsg']
                    token.status_change_at = datetime.datetime.now()
                    token.save()
                    errmsg = f"{res['errmsg']}"
                    continue
                token.status = 1
                token.status_change_at = datetime.datetime.now()
                token.save()
                return res
            else:
                self.logger.error(f"Fofa状态码错误:{res.status_code} {token.id} {res.text}")
                token.status = 2
                token.error_num = token.error_num + 1
                token.error_msg = "not 200"
                token.status_change_at = datetime.datetime.now()
                token.save()
                errmsg = f"not 200"
                continue
        return {'error': True, "result": [], 'page_size': 0, "errmsg": errmsg}

    def get(self, query_str, page=1, page_size=30):

        """
        host,title,ip,domain,port,country,province,city,country_name,
        header,server,protocol,banner,cert,isp,as_number,as_organization,latitude
        """
        # fields = "host,title,ip,domain,port,country,province,city,country_name," \
        #          "server,protocol,banner,isp,as_number,as_organization,latitude"
        fields = "host,title,ip,domain,port,country,province,city,country_name," \
                 "header,server,protocol,banner,cert,isp,as_number,as_organization,latitude,ongitude,icp,mtime"

        fields_list = fields.split(",")

        # fcoin = client.get_userinfo()["fcoin"]  # 查询F币剩余数量
        # if fcoin <= 249:
        #     break  # 当F币剩249个时，不再获取数据
        data = self.get_json_data(query_str, fields=fields, page=page, size=page_size)  # 查询第page页数据的ip和城市
        self.logger.info(f"Fofa返回数据: {json.dumps(data, ensure_ascii=False)}")
        if not data["error"]:
            items = []
            data["count"] = data['size']
            data["page_size"] = page_size
            for field in data["results"]:
                item = dict(zip(fields_list, field))
                # 标题不存在 过滤
                # if item['title']:
                item["uuid"] = md5(item["host"] + item["ip"] + item["port"])
                items.append(item)

            data.pop("results")
            data.pop("query")
            data.pop("size")
            data.pop("error")
            data.pop("mode")
            data["results"] = items

        else:
            if "401 Unauthorized" in data.get('errmsg', ""):
                self.logger.error(f"key最后错误: {data['errmsg']}")
            data['result'] = []
            data['count'] = 0
            data['errmsg'] = data.get('errmsg', "")
        return data

    def search(self, query, page=1, page_size=10):
        # try:
        if page_size > 100:
            page_size = 100

        data = self.get(query_str=query, page=page, page_size=page_size)
        # except:
        #     data = []
        return data

    def get_toekns(self):
        return FofaToken.objects.all()

    def get_asset_num(self, ip, parent_id):
        data = self.search(f'ip="{ip}"')
        count = data.get("count", 0)
        instance = Attack.objects.get(id=parent_id)
        instance.asset_num = count
        instance.save()
        return count


if __name__ == '__main__':
    fc = FofaClient()
    a = fc.search('ip="112.10.215.30"')
    # a = fc.get_asset_num(ip="112.10.215.30", parent_id=1)
    print(json.dumps(a, ensure_ascii=False))
