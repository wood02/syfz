#!/usr/bin/python3
# coding:utf-8
# @File: kafka_utils.py
# @Author:cgs
# @Time:2021/8/18 4:02 下午
# from kafka import KafkaProducer, KafkaConsumer
# def kafka_send_msg(msg):
#     try:
#         produce = KafkaProducer(bootstrap_servers=KafkaConnectionConf.bootstrap_servers)
#     except Exception as err:
#         print(err)
#         produce = None
#     if produce is not None:
#         # 发送数据
#     else:
