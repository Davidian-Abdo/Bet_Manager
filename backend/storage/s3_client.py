import boto3
from botocore.exceptions import NoCredentialsError
from core.config import settings

s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY,
    aws_secret_access_key=settings.AWS_SECRET_KEY,
    region_name=settings.AWS_REGION
)

BUCKET_NAME = settings.AWS_BUCKET_NAME

def upload_to_s3(file_path: str, key: str) -> str:
    try:
        s3.upload_file(file_path, BUCKET_NAME, key)
        return f"https://{BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"
    except NoCredentialsError:
        raise Exception("AWS credentials not found")

def delete_from_s3(key: str):
    s3.delete_object(Bucket=BUCKET_NAME, Key=key)