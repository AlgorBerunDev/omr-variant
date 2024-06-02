import pika
from src.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASS

# Подключение к локальному серверу RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Создание обменника типа 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Создание или подключение к существующей очереди с параметром durable=True
channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

# Определение маршрутного ключа и тела сообщения
routing_key = 'info'
message = 'Hello World!'

# Отправка сообщения в обменник
channel.basic_publish(exchange='direct_logs',
                      routing_key=routing_key,
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode=2,  # Делает сообщение устойчивым
                      ))
print(f" [x] Sent {routing_key}:{message}")

# Закрытие соединения
connection.close()
