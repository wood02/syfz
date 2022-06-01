# coding:utf-8
import requests

from apps.equipment.models import Equipment


def scan():

  # url_list = ["https://www.baidu.com", "http://192.168.8.2"]

  all_equipment = Equipment.objects.all()
  for equipment in all_equipment:
    # print(url)
    try:
      request = requests.get(equipment.access_url, timeout=5)
      httpStatusCode = request.status_code
      if httpStatusCode!=200:
          equipment.is_online=False
      else:
          equipment.is_online = True
      # print('测试[ {} ]是否能访问，结果为 {}'.format(equipment.access_url, httpStatusCode))
    except Exception as e:
          equipment.is_online=False
          # print('测试[ {} ]是否能访问，结果为 {}'.format(equipment.access_url, 404))
    equipment.save()