# -*- coding: utf-8 -*-
import requests
from Syfz.setup import django_setup
from apps.system.models import GlobalConfig

from common.current.log import get_logger


class IpWW:
    def __init__(self, ip, parent_id=None, is_save=True):
        self.ip = ip
        self.is_save = is_save
        self.parent_id = parent_id
        v = GlobalConfig.objects.filter(key="IPWW_CONF").first().value

        self.url = f'{v["base_url"]["url"]}?key={v["api_key"]["key"]}&ip={self.ip}&coordsys=WGS84&area=multi'
        self.get_logger = get_logger("utils", 'ipww.log', filter=lambda record: "ipww" in record["extra"])
        self.logger = self.get_logger.bind(ipww=True)

    def get(self):
        result = {}
        try:
            r = requests.request("GET", self.url, verify=False, timeout=2,
                                 proxies={'http': None, 'https': None})
            r_json = r.json()

            # r_json = {
        #     "code": "Success",
        #     "data": {
        #         "multiAreas": {
        #             "address": "",
        #             "lat": "39.902798",
        #             "lng": "116.401159",
        #             "radius": "105.2321",
        #             "prov": "北京市",
        #             "city": "北京市",
        #             "district": "朝阳区",
        #         },
        #         "continent": "亚洲",
        #         "country": "中国",
        #         "consistency": "2",
        #         "correctness": "3",
        #         "owner": "北京维瑞智盛软件开发有限公司",
        #         "isp": "北京海迅达通信有限责任公司",
        #         "zipcode": "100005",
        #         "timezone": "UTC+8",
        #         "accuracy": "城市",
        #         "source": "数据挖掘",
        #         "areacode": "CN",
        #         "asnumber": "45083",
        #     },
        #     "charge": True,
        #     "msg": "查询成功",
        #     "ip": "1.45.124.145",
        #     "coordsys": "WGS84",
        #     "area": "multi",
        # }
            if not r_json['charge']:
                self.logger.error(r_json['msg'])
            if r_json['code'] == "Success":
                result = r_json['data']
                if self.is_save:
                    self.save(result)
        except Exception as e:
            self.logger.error("ip地理位置错误：" + str(e))

        return result

    def save(self, data):
        from apps.alarm.models import DetailLocation, Attack

        DetailLocation.objects.update_or_create(**{
            "attack_id": self.parent_id,
            "location": data
        })
        instance = Attack.objects.get(id=self.parent_id)

        instance.location = data
        instance.save()


if __name__ == '__main__':
    iww = IpWW("119.188.248.40", 1)
    print(iww.get())
