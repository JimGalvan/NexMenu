import boto3
from django.conf import settings

_cached_s3_client = None


def get_s3_client():
    global _cached_s3_client
    if _cached_s3_client is None:
        _cached_s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
    return _cached_s3_client
