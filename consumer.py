import pika
from src.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASS

# Подключение к локальному серверу RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Удаление существующей очереди
channel.queue_delete(queue=RABBITMQ_QUEUE)

# Создание обменника типа 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Создание новой очереди с параметром durable=True
result = channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
queue_name = result.method.queue

# Привязка очереди к обменнику с определенным маршрутным ключом
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='info')

print(' [*] Waiting for messages. To exit press CTRL+C')

# Функция обратного вызова для обработки полученного сообщения
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")

# Указание RabbitMQ, что нужно использовать эту функцию для получения сообщений из очереди
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)

channel.start_consuming()
