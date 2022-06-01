# -*- coding: utf-8 -*-
import datetime
import time
import ntplib


def get_ntp_time():
    try:
        from Syfz.settings.config import config
        ntp_servers = config.get('NTP', 'Servers')
        ntp_servers = ntp_servers.split(",")
    except Exception:

        ntp_servers = ['cn.ntp.org.cn',
                       'time1.aliyun.com',
                       'time2.aliyun.com',
                       'time3.aliyun.com',
                       'time4.aliyun.com',
                       'time5.aliyun.com',
                       'time6.aliyun.com',
                       'time7.aliyun.com',
                       ]
    time_list = []
    for ntp_server in ntp_servers:
        try:
            time_dict = {}
            c = ntplib.NTPClient()
            response = c.request(ntp_server, version=4, timeout=1)
            localtime = datetime.datetime.now()
            localtime_unix = time.mktime(localtime.timetuple())

            local_time = localtime.strftime('%Y-%m-%d %H:%M:%S')
            tx_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(response.tx_time))
            time_dict["server"] = ntp_server
            time_dict["ntp_time"] = [response.tx_time, tx_time]
            time_dict["local_time"] = [localtime_unix, local_time]
            time_list.append(time_dict)
        except Exception:
            continue

    return time_list


if __name__ == '__main__':
    ntps = get_ntp_time()
    print(ntps)
    if ntps:
        ntp = ntps[0]['ntp_time']
        local = ntps[0]['local_time']
        print(ntp, local)

    import time
    import datetime

    dtime = datetime.datetime.now()
    ans_time = time.mktime(dtime.timetuple())
    print(ans_time)
