from consumer_base import ConsumerBase
from rabbitmq_utils import publish_message

class ResizeConsumer(ConsumerBase):
    def process_message(self, body, correlation_id):
        # Логика изменения размера изображения
        resized_image_path = 'path/to/resized_image.jpg'
        # Отправка в следующую очередь
        publish_message(self.channel, self.exchange, 'a4_format', resized_image_path, correlation_id)

if __name__ == "__main__":
    consumer = ResizeConsumer(queue='resize_queue', routing_key='resize')
    consumer.start_consuming()
