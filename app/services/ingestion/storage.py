from minio import Minio
from minio.error import S3Error
from app.core.config import settings
from app.core.exceptions import NotFoundError, ValidationError
import io

minio_client= Minio(
    settings.minio_endpoint,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=settings.minio_secure,
)

def ensure_bucket_exists():
    try:
        if not minio_client.bucket_exists(settings.minio_bucket):
            minio_client.make_bucket(settings.minio_bucket)
    except S3Error as e:
        raise ValidationError(f"Minio bucket error: {e}")


async def upload_file(file_path: str, file_data: bytes, content_type: str) -> str:
    try:
        minio_client.put_object(
            settings.minio_bucket,
            file_path,
            io.BytesIO(file_data),
            length=len(file_data),
            content_type=content_type,
        )
        return file_path
    except S3Error as e:
        raise ValidationError(f"Failed to upload file: {e}")


async def download_file(file_path: str) -> bytes:
    try:
        response = minio_client.get_object(
            settings.minio_bucket,
            file_path,
        )
        return response.read()
    except S3Error as e:
        raise NotFoundError(f"Failed to download file: {e}")
    