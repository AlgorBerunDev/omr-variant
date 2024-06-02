import os
from dotenv import load_dotenv
from consumer.consumer import start_consumer

def main():
    load_dotenv()  # Загрузка переменных окружения из .env файла
    
    # Запуск консумера
    start_consumer()

if __name__ == "__main__":
    main()
