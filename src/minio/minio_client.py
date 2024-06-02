import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from minio import Minio
from minio.error import S3Error
import cv2
import numpy as np
from io import BytesIO
from src.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

# Создание клиента MinIO
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

def download_image(image_url):
    try:
        # Загрузка изображения из MinIO
        image_path = os.path.join("/tmp", os.path.basename(image_url))
        minio_client.fget_object(MINIO_BUCKET_NAME, image_url, image_path)
        return image_path
    except S3Error as e:
        print(f"Error occurred: {e}")
        return None

def upload_image(image_path, object_name=None):
    try:
        if object_name is None:
            object_name = os.path.basename(image_path)
        # Загрузка изображения в MinIO
        minio_client.fput_object(MINIO_BUCKET_NAME, object_name, image_path)
        print(f"Image uploaded successfully: {object_name}")
        return object_name
    except S3Error as e:
        print(f"Error occurred: {e}")
        return None

def delete_image(object_name):
    try:
        # Удаление изображения из MinIO
        minio_client.remove_object(MINIO_BUCKET_NAME, object_name)
        print(f"Image deleted successfully: {object_name}")
    except S3Error as e:
        print(f"Error occurred: {e}")

def update_image(image_path, object_name):
    try:
        # Обновление изображения в MinIO
        delete_image(object_name)
        upload_image(image_path, object_name)
        print(f"Image updated successfully: {object_name}")
    except S3Error as e:
        print(f"Error occurred: {e}")

def read_image_cv2(image_url):
    try:
        # Загрузка изображения из MinIO
        image_path = download_image(image_url)
        if image_path:
            # Чтение изображения с использованием cv2
            image = cv2.imread(image_path)
            return image
        else:
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def save_image_cv2(image, image_path):
    try:
        # Сохранение изображения с использованием cv2
        cv2.imwrite(image_path, image)
        print(f"Image saved successfully: {image_path}")
        return image_path
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def upload_image_cv2(image, object_name):
    try:
        # Преобразование изображения в буфер
        is_success, buffer = cv2.imencode('.jpg', image)
        if not is_success:
            print("Failed to convert image to buffer")
            return None
        
        # Преобразование буфера в поток
        image_stream = BytesIO(buffer)
        image_stream.seek(0)
        
        # Загрузка изображения в MinIO напрямую из потока
        minio_client.put_object(
            bucket_name=MINIO_BUCKET_NAME,
            object_name=object_name,
            data=image_stream,
            length=len(buffer),
            content_type='image/jpeg'
        )
        print(f"Image uploaded successfully: {object_name}")
    except Exception as e:
        print(f"Error occurred: {e}")
