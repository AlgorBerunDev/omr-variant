import pika
from src.config import RABBITMQ_HOST, RABBITMQ_QUEUE, RABBITMQ_USER, RABBITMQ_PASS

# Подключение к локальному серверу RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
channel = connection.channel()

# Создание обменника типа 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# Создание или подключение к существующей очереди с параметром durable=True
result = channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
queue_name = result.method.queue

# Привязка очереди к обменнику с определенным маршрутным ключом
channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key='info')

print(' [*] Waiting for messages. To exit press CTRL+C')

# Функция обратного вызова для обработки полученного сообщения
def callback(ch, method, properties, body):
    try:
        print(f" [x] Received {body} with correlation_id {properties.correlation_id}")
        # Здесь можно добавить логику обработки сообщения
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Подтверждение успешной обработки
        print(f" [x] Task with correlation_id {properties.correlation_id} completed successfully")
    except Exception as e:
        print(f" [x] Task with correlation_id {properties.correlation_id} failed: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)  # Подтверждение неуспешной обработки

# Указание RabbitMQ, что нужно использовать эту функцию для получения сообщений из очереди
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=False)  # Отключаем auto_ack для ручного подтверждения

channel.start_consuming()
