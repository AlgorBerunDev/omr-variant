import pika
from rabbitmq_utils import get_rabbitmq_connection, setup_exchange_and_queue

class ConsumerBase:
    def __init__(self, queue, routing_key, exchange='image_processing', exchange_type='direct'):
        self.queue = queue
        self.routing_key = routing_key
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = get_rabbitmq_connection()
        self.channel = self.connection.channel()
        setup_exchange_and_queue(self.channel, self.exchange, self.exchange_type, self.queue, self.routing_key)

    def start_consuming(self):
        self.channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=False)
        print(f' [*] Waiting for messages in {self.queue}. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        try:
            print(f" [x] Received {body} with correlation_id {properties.correlation_id}")
            self.process_message(body, properties.correlation_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f" [x] Task with correlation_id {properties.correlation_id} completed")
        except Exception as e:
            print(f" [x] Task with correlation_id {properties.correlation_id} failed: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def process_message(self, body, correlation_id):
        raise NotImplementedError("Subclasses must implement this method")
