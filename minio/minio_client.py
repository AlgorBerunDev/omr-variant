import cv2
from minio import Minio
from minio.error import S3Error
import os
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
