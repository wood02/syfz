# -*- coding: utf-8 -*-
import datetime
import json
import os
from json import JSONDecodeError

from tenacity import retry, stop_after_attempt, wait_random

from Syfz.setup import *
import pika
import sys

# https://medium.com/@rahulsamant_2674/python-rabbitmq-8c1c3b79ab3d
from apps.alarm.models import Attack
from apps.tracesource.models import TsServer
from common.current.log import get_logger

get_logger = get_logger("ts", 'consumer_ts_server.log',
                        filter=lambda record: "consumer_ts_server" in record["extra"])
logger = get_logger.bind(consumer_ts_server=True)


class Subscriber:
    """
    溯源扫描服务器状态
    """

    def __init__(self, queueName, bindingKey, config):
        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.connection = self._create_connection()
        self.min = 1
        self.max = 5

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(username=self.config['username'], password=self.config['password'])
        parameters = pika.ConnectionParameters(host=self.config['host'],
                                               port=self.config['port'],
                                               client_properties={
                                                   'connection_name': "consumer2",
                                               },
                                               credentials=credentials)
        return pika.BlockingConnection(parameters)

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key

        logger.info("Received new message from - " + binding_key)
        body = str(body, 'UTF-8')
        logger.warning("Received %r" % body)
        self.save2db(body)

    def save2db(self, d):
        # try:
        from django.db import close_old_connections
        close_old_connections()
        logger.warning("Saving to DB")
        d = json.loads(d)
        # data = d['data']
        # {"ip": {"local_ip": local_ip, "public_ip": public_ip}, "server_type": SERVER_TYPE, "status": STATUS}
        public_ip = d['ip']['public_ip']
        if public_ip:
            TsServer.objects.update_or_create(**{"ip": d['ip']['public_ip'], "server_type": d['server_type']},
                                              defaults={"status": d['status'], "cpu_rate": d['cpu_rate'],
                                                        "mem_rate": d['mem_rate']})
        logger.warning("Saved to DB")

    # except Exception as e:
    #     logger.error("数据存储异常：" + str(e))

    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='topic')
        channel.queue_declare(queue=self.queueName)
        channel.queue_bind(queue=self.queueName, exchange=self.config['exchange'], routing_key=self.bindingKey)
        channel.basic_consume(queue=self.queueName,
                              on_message_callback=self.on_message_callback, auto_ack=True)
        logger.warning(f'已连接， Waiting for queue: [ {self.queueName} ] routing_key: [ {self.bindingKey} ]')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()


# @retry(wait=wait_random(min=1, max=2))
def run():
    # try:
    logger.info("consumer2 start")
    MQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
    MQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
    MQ_USER = os.getenv("RABBITMQ_USER", "admin")
    MQ_PSW = os.getenv("RABBITMQ_PASS", "Fxs2021@")

    config = {'host': MQ_HOST, 'port': MQ_PORT, 'username': MQ_USER, 'password': MQ_PSW,
              'exchange': 'exchange_new_scan_server'}

    subscriber = Subscriber('queue_new_scan_server', 'topic_new_scan_server', config)
    subscriber.setup()


# except Exception as e:
#     logger.error(f"连接异常，重新连接：{e}")
#     raise Exception("连接异常，重新连接")


if __name__ == '__main__':
    run()
