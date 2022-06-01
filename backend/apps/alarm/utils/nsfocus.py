# -*- coding: utf-8 -*-

from Syfz.setup import django_setup
import datetime

import requests

from apps.alarm.models import XtbApiKey, NsfocusApiKey
from common.current.log import get_logger
from common.utils.desutil import DEncry
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class NsfocusCilent:  # 绿盟
    def __init__(self, ip, parent_id):
        self.des = DEncry()
        self.ip = ip
        self.url = "https://ti.nsfocus.com/api/v2/objects/ioc-ipv4/"
        self.parent_id = parent_id

        self.get_logger = get_logger("utils", 'nsfocus.log', filter=lambda record: "nsfocus" in record["extra"])
        self.logger = self.get_logger.bind(nsfocus=True)

    def get_apikey(self):
        """
        获取可用值 和重置用例
        """
        keys = NsfocusApiKey.objects.all()
        result = []
        for key in keys:
            api_reset_at = key.api_reset_at
            if api_reset_at.strftime("%Y-%m-%d") != datetime.datetime.now().strftime("%Y-%m-%d"):
                print("不是同一天")
                key.api_reset_at = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
                key.api_remaining = 50
                key.api_limit = 50
                key.error_num = 0
                key.save()
            # if tag.status != 3 and tag.api_remaining > 0:
            if key.error_num <= 10 and key.api_remaining > 0:
                result.append(key)
        if len(result) == 0:
            self.logger.error("没有可用的绿盟apikey")

        return result

    def __client(self):
        apikeys = self.get_apikey()
        for key in apikeys:
            apikey = self.des.decrypt(key.apikey)
            header = {"Accept": "application/nsfocus.nti.spec+json; version=2.0",
                      "X-Ns-Nti-Key": "f31e580eb4833543b719f6919c644873433edf2f9fabba5d8be154d1075de56e",
                      "Accept-encoding": "gzip"}

            try:
                data = {"query": self.ip}
                r = requests.get(self.url, params=data, headers=header)
                if r.status_code == 200:

                    r_json = r.json()

                    if r_json['response_code'] != 0:
                        key.status = 2
                        key.status_change_at = datetime.datetime.now()
                        key.error_msg = r_json['verbose_msg']
                        key.error_num += 1
                        key.save()
                        self.logger.error('绿盟 API 调用失败，错误信息：%s' % r_json['verbose_msg'])
                        return {}
                    key.status = 1
                    key.status_change_at = datetime.datetime.now()
                    key.api_remaining = key.api_remaining - 1
                    key.save()
                    return r_json
                else:
                    key.status = 3
                    key.status_change_at = datetime.datetime.now()
                    key.error_msg = r.status_code
                    key.error_num += 1
                    key.save()
                    self.logger.error('绿盟 API 调用失败，错误码：%s' % r.status_code)
                    return {}
            except Exception as e:
                self.logger.error("连接错误！")
                key.status = 2
                key.status_change_at = datetime.datetime.now()
                key.error_msg = str(e)
                key.error_num += 1
                key.save()
            return {}
        return {}

    def get(self):

        result = {}
        success = True
        try:
            r_json = self.__client()
            if r_json:
                result = r_json['objects']

        except Exception as e:
            self.logger.error('查询 %s 的绿盟信息发生错误，错误信息：%s' % (self.ip, repr(e)))
            success = False
        self.save(result)
        return result, success

    def save(self, data):
        from apps.alarm.models import DetailTagInfo
        # data = {
        #     "count": 3,
        #     "spec_version": "2.0",
        #     "objects": [
        #         {
        #             "confidence": 100,
        #             "threat_level": 3,
        #             "revoked": False,
        #             "pattern": "[ipv4-addr:value = '117.188.0.77']",
        #             "tags": [
        #                 {
        #                     "tag_values": [
        #                         "inbound"
        #                     ],
        #                     "tag_type": "direction"
        #                 }
        #             ],
        #             "modified": "2020-05-26T02:06:26.000Z",
        #             "created_by": "nsfocus",
        #             "observables": [
        #                 {
        #                     "type": "ipv4-addr",
        #                     "value": "117.188.0.77"
        #                 }
        #             ],
        #             "threat_types": [
        #                 401
        #             ],
        #             "act_types": [
        #                 0
        #             ],
        #             "type": "indicator",
        #             "id": "0c9010cf5ecbcacc030f1",
        #             "categories": [
        #                 "ip"
        #             ]
        #         },
        #         {
        #             "confidence": 50,
        #             "threat_level": 5,
        #             "revoked": False,
        #             "pattern": "[ipv4-addr:value = '117.188.0.77']",
        #             "tags": [
        #                 {
        #                     "tag_values": [
        #                         "inbound"
        #                     ],
        #                     "tag_type": "direction"
        #                 }
        #             ],
        #             "modified": "2020-04-07T01:06:45.000Z",
        #             "created_by": "nsfocus",
        #             "observables": [
        #                 {
        #                     "type": "ipv4-addr",
        #                     "value": "117.188.0.77"
        #                 }
        #             ],
        #             "threat_types": [
        #                 5
        #             ],
        #             "act_types": [
        #                 0
        #             ],
        #             "type": "indicator",
        #             "id": "0c9012f05e8b5cd5030f1",
        #             "categories": [
        #                 "ip"
        #             ]
        #         },
        #         {
        #             "confidence": 80,
        #             "threat_level": 5,
        #             "revoked": False,
        #             "pattern": "[ipv4-addr:value = '117.188.0.77']",
        #             "tags": [
        #                 {
        #                     "tag_values": [
        #                         "inbound"
        #                     ],
        #                     "tag_type": "direction"
        #                 }
        #             ],
        #             "modified": "2020-05-25T22:06:08.000Z",
        #             "created_by": "nsfocus",
        #             "observables": [
        #                 {
        #                     "type": "ipv4-addr",
        #                     "value": "117.188.0.77"
        #                 }
        #             ],
        #             "threat_types": [
        #                 405
        #             ],
        #             "act_types": [
        #                 0
        #             ],
        #             "type": "indicator",
        #             "id": "0c9010585ecbcac7030f1",
        #             "categories": [
        #                 "ip"
        #             ]
        #         }
        #     ],
        #     "type": "bundle"
        # }
        # data = data['objects']
        DetailTagInfo.objects.update_or_create(**{
            "attack_id": self.parent_id,

            'source': 2,
        }, defaults={"tag_info": data})


if __name__ == '__main__':
    from Syfz.setup import django_setup

    tb = NsfocusCilent(ip="127.0.0.1", parent_id=1)
    a = tb.get()
    # tb.save(data="")
    # print(a)

