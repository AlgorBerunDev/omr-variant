import uuid
from rabbitmq_utils import get_rabbitmq_connection, publish_message

def main():
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    exchange = 'image_processing'
    routing_key = 'resize'
    message = 'path/to/image.jpg'
    correlation_id = str(uuid.uuid4())

    publish_message(channel, exchange, routing_key, message, correlation_id)
    print(f" [x] Sent {routing_key}:{message} with correlation_id {correlation_id}")

    connection.close()

if __name__ == "__main__":
    main()
