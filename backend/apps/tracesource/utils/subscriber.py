# -*- coding: utf-8 -*-
import json

import pika
import sys


# https://medium.com/@rahulsamant_2674/python-rabbitmq-8c1c3b79ab3d


class Subscriber:
    def __init__(self, queueName, bindingKey, config):
        self.queueName = queueName
        self.bindingKey = bindingKey
        self.config = config
        self.connection = self._create_connection()

    def __del__(self):
        self.connection.close()

    def _create_connection(self):
        credentials = pika.PlainCredentials(username=self.config['username'], password=self.config['password'])
        parameters = pika.ConnectionParameters(host=self.config['host'],
                                               port=self.config['port'],
                                               credentials=credentials)
        return pika.BlockingConnection(parameters)

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key

        print("received new message for -" + binding_key)
        print(" [x] Received %r" % body)

        self.save(json.loads(body.decode("utf-8")))

    def setup(self):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.config['exchange'],
                                 exchange_type='topic')
        channel.queue_declare(queue=self.queueName)
        channel.queue_bind(queue=self.queueName, exchange=self.config['exchange'], routing_key=self.bindingKey)
        channel.basic_consume(queue=self.queueName,
                              on_message_callback=self.on_message_callback, auto_ack=True)
        print('[*] Waiting for data for ' + self.queueName + '. To exit press CTRL+C')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()

    def save(self, data):
        from Syfz.setup import django_setup
        from apps.tracesource.models import TsServer
        print("saving data", data)
        TsServer.objects.update_or_create(**{"ip": data['ip']['public_ip']}, defaults={"server_type": data['server_type']})


def parse_config():
    MQ_HOST = '127.0.0.1'
    MQ_PORT = 5672
    MQ_USER = "admin"
    MQ_PSW = 'Fxs2021@'

    config = {'host': MQ_HOST, 'port': MQ_PORT, 'username': MQ_USER, 'password': MQ_PSW, 'exchange': 'my_exchange'}

    subscriber = Subscriber('queue_new_scan_server', 'topic_new_scan_server', config)
    subscriber.setup()


if __name__ == '__main__':
    parse_config()
