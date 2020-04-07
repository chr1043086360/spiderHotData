from core.settings import KAFKA_HOST_IP_PORT
from kafka import KafkaProducer
import json


def Kafka_producer(data):
    producer = KafkaProducer(
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        bootstrap_servers=[f"{KAFKA_HOST_IP_PORT}"]
    )

    producer.send('spider', data)
    producer.close()
