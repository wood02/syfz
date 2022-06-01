# -*- coding: utf-8 -*-
Q_CLUSTER = {
    'name': 'Syfz',  # 项目名称
    'workers': 4,  # worker数。默认为当前主机的CPU计数，
    'recycle': 500,  # worker在回收之前要处理的任务数。有助于定期释放内存资源。默认为500。
    'timeout': 3 * 60,  # 任务超时设置,如果是爬虫任务建议设置长一些
    'retry': 5 * 60,  # 任务重试时间
    'max_attempts': 3,  # 最大尝试次数
    'compress': True,  # 数据压缩
    'save_limit': 250,  # 限制保存到Django的成功任务的数量。0为无限，-1则不会保存
    'queue_limit': 100,  # 排队的任务数量，默认为workers**2。
    'cpu_affinity': 1,  # 设置每个工作人员可以使用的处理器数量。根据经验; cpu_affinity 1支持重复的短期运行任务，而没有亲和力则有利于长时间运行的任务。
    'label': 'Django Q',  # 用于Django Admin页面的标签。默认为'Django Q'，之后我会根据源码做一个中文版的django-admin页面。如果有需求请私信我
    'redis': {
        'host': 'localhost',
        'port': 6379,
        'db': 9,
        'password': None,
        'socket_timeout': None,
        'charset': 'utf-8',
        'errors': 'strict',
        'unix_socket_path': None
    }
}
