import pika
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASS

def process_message(ch, method, properties, body):
    message = json.loads(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=process_message)
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

start_consumer()
