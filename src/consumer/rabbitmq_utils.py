import pika
from src.config import RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASS

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
    return connection

def setup_exchange_and_queue(channel, exchange, exchange_type, queue, routing_key):
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(exchange=exchange, queue=queue, routing_key=routing_key)

def publish_message(channel, exchange, routing_key, message, correlation_id):
    channel.basic_publish(exchange=exchange,
                          routing_key=routing_key,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # Делает сообщение устойчивым
                              correlation_id=correlation_id
                          ))
