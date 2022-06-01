# -*- coding: utf-8 -*-
from Syfz.setup import django_setup

import os.path
import re
import requests
from fake_useragent import UserAgent

from requests.adapters import HTTPAdapter

from Syfz.settings import BASE_DIR
from apps.alarm.models import Attack
from common.current.log import get_logger

requests.packages.urllib3.disable_warnings()  # 抑制https错误信息


class IP2Domain:
    def __init__(self, ip, parent_id):
        self.useragent = UserAgent(path=os.path.join(BASE_DIR, 'fake_useragent_0.1.11.json')).random
        self.thread = 3
        self.ip = ip
        self.parent_id = parent_id
        self.get_logger = get_logger("utils", 'ip2domain.log', filter=lambda record: "ip2domain" in record["extra"])
        self.logger = self.get_logger.bind(ip2domain=True)

    # vvhan查询备案信息
    def searchRecordByVvhan(self, domain):
        header = {
            "user-agent": self.useragent
        }
        resultDic = {
            'name': '',
            'nature': '',
            'icp': '',
            'title': '',
            'time': ''
        }
        try:
            s = requests.Session()
            # 重试次数为3
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            # 超时时间为5s
            rep = s.get(url=f"https://api.vvhan.com/api/icp?url={domain}", headers=header, timeout=3)
            return rep.json()['info']
        except:
            return resultDic

    # devopsclub 查询whois信息
    def whoIs(self, domain):

        headers = {"user-agent": self.useragent}
        # whois查询
        result = {
            "contactEmail": "",
            "contactPhone": "",
            "dnsNameServer": [
            ],
            "domainName": "",
            "domainStatus": "",
            "expirationTime": "",
            "registrant": "",
            "registrar": "",
            "registrarWHOISServer": "",
            "registrationTime": "",
            "updatedDate": ""
        }
        try:
            s = requests.Session()
            # 重试次数为3
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            url = 'https://api.devopsclub.cn/api/whoisquery?domain=%s&type=json' % domain
            r = s.get(url, headers=headers)
            json_obj = r.json()
            if json_obj['data']['status'] == 0:
                return json_obj['data']['data']
        except Exception:
            return result

    # webscan反查域名
    def searchDomain(self):
        headers = {"user-agent": self.useragent}
        domainInfo = []
        try:
            rep = requests.get(url=f"http://api.webscan.cc/?action=query&ip={self.ip}", headers=headers, timeout=5)
            if rep.text != "null":
                results = rep.json()
                for result in results:
                    domainName = result["domain"]
                    if re.match(
                            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",
                            domainName):
                        continue

                    icpDataDic = self.searchRecordByVvhan(domainName)
                    whoisDataDic = self.whoIs(domainName)
                    domain_all = result

                    domain_all['icp'] = icpDataDic if icpDataDic else {}
                    domain_all['whois'] = whoisDataDic if whoisDataDic else {}

                    domainInfo.append(domain_all)
                    # break
        except Exception as e:
            self.logger.error(f"ip2domain searchDomain error: {str(e)}")
        self.save(domainInfo)
        return domainInfo

    def save(self, data):
        from apps.alarm.models import DetailDomain

        DetailDomain.objects.update_or_create(**{
            "attack_id": self.parent_id,
            "domain": data,
        })
        instance = Attack.objects.get(id=self.parent_id)
        instance.domain_num = len(data)
        instance.is_ip2_domain = True
        instance.save()


if __name__ == "__main__":
    # itod = IP2Domain('58.218.208.13', 1)
    # itod = IP2Domain('202.107.201.3', 1)
    itod = IP2Domain('124.221.154.15', 1)
    a = itod.searchDomain()
    print(a)
