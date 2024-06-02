from consumer_base import ConsumerBase
from rabbitmq_utils import publish_message

class A4FormatConsumer(ConsumerBase):
    def process_message(self, body, correlation_id):
        # Логика анализа формата A4 и wrap
        a4_image_path = 'path/to/a4_image.jpg'
        # Отправка в две очереди параллельно
        publish_message(self.channel, self.exchange, 'coordinate_analysis', a4_image_path, correlation_id)
        publish_message(self.channel, self.exchange, 'block_id_analysis', a4_image_path, correlation_id)

if __name__ == "__main__":
    consumer = A4FormatConsumer(queue='a4_format_queue', routing_key='a4_format')
    consumer.start_consuming()
