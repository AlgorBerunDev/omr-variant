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
