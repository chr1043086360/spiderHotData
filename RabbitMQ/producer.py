import pika
import json
from core.settings import RABBITMQ_HOST_IP, RABBITMQ_PASSWORD


def RabbitMQ_producer(data):
    credentials = pika.PlainCredentials('root', f'{RABBITMQ_PASSWORD}')  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(pika.ConnectionParameters(host = f'{RABBITMQ_HOST_IP}',port = 5672,virtual_host = '/',credentials = credentials))
    channel=connection.channel()
    # 声明消息队列，消息将在这个队列传递，如不存在，则创建
    result = channel.queue_declare(queue = 'spider')

    for i in range(10):
        message=json.dumps(data)
        # 向队列插入数值 routing_key是队列名
        channel.basic_publish(exchange = '',routing_key = 'spider',body = message)
        # print(message)
    connection.close()