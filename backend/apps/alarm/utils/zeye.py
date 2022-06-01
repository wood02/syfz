#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64

from Syfz.setup import django_setup
from common.utils.desutil import DEncry

from apps.alarm.models import ZoomEyeToken
import json
from zoomeye.sdk import ZoomEye
from common.current.log import get_logger

from common.utils.md5 import md5

des = DEncry()


class ZeyeClient:
    def __init__(self, tokens=None):
        self.tokens = tokens if tokens else self.get_token()
        self.get_logger = get_logger("utils", 'zoomeye.log', filter=lambda record: "zoomeye" in record["extra"])
        self.logger = self.get_logger.bind(zoomeye=True)
        # self.get_userinfo()  # check email and key

    def get_token(self):
        return ZoomEyeToken.objects.all()

    def resources(self):
        z_list = []
        for token_obj in self.tokens:
            token = des.decrypt(token_obj.token)
            # print(token)
            try:
                zm = ZoomEye(api_key=token)
                resources_info = zm.resources_info()
                resources_info.pop("user_info")
                remain_total_quota = resources_info['quota_info']['remain_total_quota']
                if remain_total_quota <= 200:
                    self.logger.info(f"[Zoomeye] ID: {token_obj.id} token异常, 余量不足！")
                    token_obj.status = 2
                    token_obj.error_message = "余量不足！"
                else:
                    self.logger.info(f"[Zoomeye] ID: {token_obj.id} token正常, 余量为：{remain_total_quota}！")
                    token_obj.status = 1
                    token_obj.rate_limit = resources_info
                    token_obj.error_message = f"[Zoomeye] token正常, 余量为：{remain_total_quota}！"
                    z_list.append(zm)
            except Exception as e:
                self.logger.info(f"[Zoomeye] ID: {token_obj.id} token异常  {str(e)}")
                token_obj.status = 2
                token_obj.error_message = str(e)
            token_obj.save()

        if z_list:
            return z_list[0]
        else:
            self.logger.error("[Zoomeye] 无可用token")
            return False

    def get(self, query_str, page=1, multi=False):
        data = {}
        bytes_query = query_str.encode("utf-8")
        qbase64 = base64.b64encode(bytes_query).decode()  # 被编码的参数必须是二进制数据
        data["error"] = False
        data['query'] = query_str
        data['qbase64'] = qbase64
        data['source'] = "ZoomEye"
        zm = self.resources()
        if zm:
            if multi:
                # 前多少页
                resp = zm.multi_page_search(dork=query_str, page=page, resource="web", facets=None)
            else:
                resp = zm.dork_search(dork=query_str, page=page, resource="web", facets=None)
            for res in resp:
                try:
                    res['uuid'] = md5(str(res["ip"]) + res["site"])
                    res['ip'] = res['ip'][0] if (res['ip'] and isinstance(res['ip'], list)) else res['ip']
                    res['title'] = res['title_new'][0] if (res['title_new'] and isinstance(res['title_new'], list)) else \
                        res['title']
                    res['organization'] = res['geoinfo']["organization"] if (
                            res['geoinfo'] and isinstance(res['geoinfo'], dict) and res['geoinfo'].get(
                        "organization")) else ""
                    for i in ["raw_data", "headers", "ssl"]:
                        if i in res.keys():
                            del res[i]
                except KeyError:
                    resp.remove(res)
            data["items"] = resp
        else:
            data["items"] = []
        return data


if __name__ == '__main__':
    tokens = ZoomEyeToken.objects.all()
    client = ZeyeClient(tokens, )
    # query = 'iconhash:"-1216359276"'
    query = 'title:"杭州" +title:"上海"'
    # +ip: "156.240.109.234" + port:"80" + after: "2021-01-25 16:37:59"
    data = client.get(query_str=query)

    print(json.dumps(data, ensure_ascii=False))
