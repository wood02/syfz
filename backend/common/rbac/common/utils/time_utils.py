import datetime
# from datetime import datetime

class TimeUtils(object):

    @classmethod
    def get_today_time_str(cls):
        """
        获取当前时间字符串
        :return: 当前时间字符串
        """
        return str(datetime.datetime.now()).split('.')[0]

    @classmethod
    def get_today_datetime(cls):
        """
        获取当前时间对象
        :return:
        """
        return datetime.datetime.now()

    @classmethod
    def str_to_dt(cls, time_str):
        """
        时间戳字符串转时间戳
        :param: 要转换的str
        :return: 时间戳
        """
        dt = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return dt

    @classmethod
    def dt_to_str(cls, datetime_obj):
        """

        :param: 要转换的时间datetime对象
        :return: 时间戳
        """
        dt_str = datetime.datetime.strftime (datetime_obj, '%Y-%m-%d %H:%M:%S')
        return dt_str

    @classmethod
    def time1_ge_time2(cls, time_str1, time_str2):
        """
        对比第一个时间是否大于第二个时间
        :param time_str1: 第一个时间字符串 格式为 %Y-%m-%d %H:%M:%S
        :param time_str2: 第而个时间字符串 格式为 %Y-%m-%d %H:%M:%S
        :return: bool
        """
        return cls.str_to_dt(time_str1).__ge__(cls.str_to_dt(time_str2))

    @classmethod
    def time_add_together(cls, datetime_obj, add_num, unit=3):
        """

        :param datetime_obj: 要相加的datetime对象
        :param add_num: 要相加的数量
        :param unit: 单位(0:天,1:时,2:分,3:秒)
        :return:
        """
        # now = datetime.datetime.now()
        if unit == 0:
            add_time = datetime.timedelta(days=add_num)
        elif unit == 1:
            add_time = datetime.timedelta(hours=add_num)
        elif unit == 2:
            add_time = datetime.timedelta(minutes=add_num)
        else:
            add_time = datetime.timedelta(seconds=add_num)
        n_days = datetime_obj + add_time
        new_date_str = n_days.strftime('%Y-%m-%d %H:%M:%S')
        return new_date_str