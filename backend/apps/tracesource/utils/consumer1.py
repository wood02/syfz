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
from apps.tracesource.utils.parse_data import parse
from common.current.log import get_logger

get_logger = get_logger("ts", 'consumer.log',
                        filter=lambda record: "consumer" in record["extra"])
logger = get_logger.bind(consumer=True)


class Subscriber:
    """
    监听反制结果
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
                                                   'connection_name': "consumer1",
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
        data = d['data']
        if d['status'] == 1 or d['status'] == 2:
            attack = Attack.objects.filter(source_ip=data['target'])
            if attack:
                if d.get("finished", False):
                    logger.warning("Fz Finished")
                    attack.update(fz_status=2, fz_end_time=datetime.datetime.now(), fz_result_raw=d)
                else:
                    logger.warning("Fz-ing")
                    attack.update(fz_result_raw=d)

                parse(d['data'], logger)
            else:
                logger.warning("No such attack")
        else:
            Attack.objects.filter(source_ip=data['target']).update(fz_result_raw=d)
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
    logger.info("consumer1 start")
    MQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
    MQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
    MQ_USER = os.getenv("RABBITMQ_USER", "admin")
    MQ_PSW = os.getenv("RABBITMQ_PASS", "Fxs2021@")

    config = {'host': MQ_HOST, 'port': MQ_PORT, 'username': MQ_USER, 'password': MQ_PSW,
              'exchange': 'exchange_scan_result'}

    subscriber = Subscriber('queue_scan_result', 'topic_scan_result', config)
    subscriber.setup()


# except (KeyError, JSONDecodeError) as e:
#     logger.error(f"数据存储异常：{e}")
# except Exception as e:
#     logger.error(f"连接异常，重新连接：{e}")
#     raise Exception("连接异常，重新连接")


if __name__ == '__main__':
    run()
