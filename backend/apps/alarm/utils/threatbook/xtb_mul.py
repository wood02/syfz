# -*- coding: utf-8 -*-
import json
import logging

from Syfz.setup import django_setup
import datetime

import requests

from apps.alarm.models import XtbApiKey, Attack
from apps.alarm.models import DetailTagInfo
from common.current.log import get_logger
from common.utils.desutil import DEncry
import urllib3
from tenacity import retry, retry_if_result, stop_after_delay, stop_after_attempt, RetryError, wait_fixed, wait_random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ThreatBookMul:  # 微步威胁批量情报查询
    def __init__(self, mul_data, url, is_mul=True, is_adv=False):
        self.des = DEncry()
        self.mul_data = mul_data[:1] if not is_mul or is_adv else mul_data
        self.url = url
        self.is_adv = is_adv

        self.get_logger = get_logger("utils", 'threatbook.log',
                                     filter=lambda record: "threatbook" in record["extra"])
        self.logger = self.get_logger.bind(threatbook=True)

    def get_apikey(self):
        """
        获取可用值 和重置用例
        """
        keys = XtbApiKey.objects.all()
        result = []
        for key in keys:
            api_reset_at = key.api_reset_at
            if api_reset_at.strftime("%Y-%m-%d") != datetime.datetime.now().strftime("%Y-%m-%d"):
                print("不是同一天")
                key.api_reset_at = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
                key.api_remaining = 10000
                key.api_limit = 10000
                key.error_num = 0
                key.save()
            # if tag.status != 3 and tag.api_remaining > 0:
            if key.error_num <= 1000 and key.api_remaining > 0:
                result.append(key)

        return result

    @retry(stop=stop_after_attempt(3))
    def __client(self, query):
        apikeys = self.get_apikey()
        err_total = 0
        for key in apikeys:
            apikey = self.des.decrypt(key.apikey)
            query = {
                "apikey": apikey,
                "resource": ",".join([m["ip"] for m in self.mul_data]),
                "lang": "zh"
                , **query
            }

            self.logger.info(f'{"/".join(self.url.split("/")[-2:])} 请求参数:{query["resource"]}')
            try:
                r = requests.request("GET", self.url, params=query, verify=False,
                                     proxies={'http': None, 'https': None})
                r_json = r.json()
                # r_json = {"data": {self.ip: {"severity": "低", "judgments": ["傀儡机", "垃圾邮件", "IDC服务器", "扫描", "漏洞利用"],
                #                              "tags_classes": [], "basic": {"carrier": "中国联通",
                #                                                            "location": {"country": "中国",
                #                                                                         "province": "山东省",
                #                                                                         "city": "枣庄市",
                #                                                                         "lng": "117.266998",
                #                                                                         "lat": "34.802818",
                #                                                                         "country_code": "CN"}},
                #                              "asn": {"rank": 3,
                #                                      "info": "CHINA169-BACKBONE CHINA UNICOM China169 Backbone, CN",
                #                                      "number": 4837}, "scene": "数据中心", "confidence_level": "低",
                #                              "is_malicious": True, "update_time": "2021-11-15 17:24:13"}},
                #           "response_code": 0, "verbose_msg": "成功"}
                if r_json['response_code'] != 0:
                    key.status = 2
                    key.status_change_at = datetime.datetime.now()
                    key.error_msg = r_json['verbose_msg']
                    key.error_num += 1
                    key.save()
                    self.logger.error(f'{"/".join(self.url.split("/")[-2:])} 错误信息：%s' % r_json['verbose_msg'])
                    if r_json['verbose_msg'] == "无效的访问IP":
                        err_total += 1
                        continue

                key.status = 1
                key.status_change_at = datetime.datetime.now()
                key.api_remaining = key.api_remaining - 1
                key.save()
                return r_json

            except Exception as e:
                self.logger.error(f'{"/".join(self.url.split("/")[-2:])}微步API调用失败，连接错误！')
                key.status = 2
                key.status_change_at = datetime.datetime.now()
                key.error_msg = str(e)
                key.error_num += 1
                key.save()
        if err_total == len(self.get_apikey()) and err_total != 0:
            # 特殊处理
            raise RuntimeError("微步API调用失败，无效的访问IP")
        return {}

    def parse(self, save_to=None, query=None):
        """
        解析数据基础
        :param query: 新参数
        :param save_to: 保存到指定数据库的对象
        :return:
        """
        if query is None:
            query = {}
        success = True
        r_json = {}
        try:
            if self.is_adv:
                # todo 判断是否是高级数据 如果是高级数据 则调用高级数据的解析方法 暂无测试数据
                # r_json = {
                #     "data": {
                #         "ip": "159.203.93.255",
                #         "basic": {},
                #         "asn": {
                #             "rank": 2,
                #             "info": "DIGITALOCEAN-ASN - DigitalOcean, LLC, US",
                #             "number": 14061
                #         },
                #         "cur_domains": [],
                #         "history_domains": {
                #             "2017-02-22": [
                #                 "www.muusick.net",
                #                 "muusick.net"
                #             ],
                #             "2017-01-29": [
                #                 "www.muusick.net",
                #                 "www.muusick.tv",
                #                 "muusick.net"
                #             ],
                #             "2016-12-21": [
                #                 "www.muusick.net",
                #                 "muusick.tv",
                #                 "www.muusick.tv",
                #                 "muusick.net"
                #             ],
                #             "2016-09-11": [
                #                 "www.muusick.net",
                #                 "muusick.net"
                #             ],
                #             "2015-12-17": [
                #                 "daysntowers.com"
                #             ]
                #         }
                #     },
                #     "response_code": 0,
                #     "verbose_msg": "OK"
                # }
                r_json = self.__client(query=query)
            else:
                r_json = self.__client(query=query)
            # 如果保存到数据库
            if save_to:
                for m in self.mul_data:
                    if self.is_adv:
                        # 如果是高级数据
                        save_to(r_json['data'], m['parent_id'])
                    else:
                        save_to(r_json['data'][m['ip']], m['parent_id'])
        except (RuntimeError, RetryError) as e:
            # 为了抛出错误重试
            raise RuntimeError("无效的访问IP")
        except Exception as e:
            self.logger.error(f'{"/".join(self.url.split("/")[-2:])} 错误信息：{repr(e)}')
            success = False
        return r_json, success

    def save2tag(self, d, parent_id):
        Attack.objects.filter(id=parent_id).update(malicious=d['is_malicious'], judgments=d['judgments'],
                                                   is_tag_info=True)
        DetailTagInfo.objects.update_or_create(**{
            "attack_id": parent_id,
            "source": 1
        }, defaults={"tag_info": d})

    def save2ports(self, d, parent_id):
        DetailTagInfo.objects.update_or_create(**{
            "attack_id": parent_id,
            "source": 1
        }, defaults={"ports": d.get("ports", [])})
        Attack.objects.filter(id=parent_id).update(is_ip_query=True)

    def save2domains(self, d, parent_id):
        DetailTagInfo.objects.update_or_create(**{
            "attack_id": parent_id,
            "source": 1
        }, defaults={"cur_domains": d['cur_domains'], 'history_domains': d['history_domains']})
        Attack.objects.filter(id=parent_id).update(is_ip_query=True)


if __name__ == '__main__':
    from Syfz.setup import django_setup

    mul_data = [
        {"ip": "192.186.1.2", "parent_id": 1},
        {"ip": "13.75.68.24", "parent_id": 3},
    ]
    # url = "https://api.threatbook.cn/v3/ip/query"  # 测试端口
    url = "https://api.threatbook.cn/v3/scene/ip_reputation"
    # url = "https://api.threatbook.cn/v3/ip/adv_query"  # 测试查询 高级查询主要是当前指向该IP的域名
    # url = "https://api.threatbook.cn/v3/domain/query"  # 测试域名
    print(url)
    if "ip/query" in url:
        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False)
        save_to = tb.save2ports
    elif "scene/ip_reputation" in url:
        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=True)
        save_to = tb.save2tag
    elif "ip/adv_query" in url:
        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False, is_adv=True)
        save_to = tb.save2domains
    elif "domain/query" in url:
        mul_data = [
            {"ip": "x.threatbook.cn"},
        ]
        tb = ThreatBookMul(mul_data=mul_data, url=url, is_mul=False, is_adv=False)
        save_to = None
    a = tb.parse(save_to=save_to)
    print(json.dumps(a[0], indent=3, ensure_ascii=False))
    print(a[1])
    {
        "base_url": {"url": "https://api.threatbook.cn", "name": "基础"},
        "ip_query": {"uri": "/v3/ip/query", "name": "ip分析"},
        "ip_reputation": {"uri": "/v3/scene/ip_reputation", "name": "ip信誉"},
        "ip_adv_query": {"uri": "/v3/ip/adv_query", "name": "ip高级分析"},
        "domain_query": {"uri": "/v3/domain/query", "name": "域名分析"},
    }
