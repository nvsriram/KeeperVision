from os import getenv
import boto3
import tempfile
from botocore.exceptions import ClientError


def get_s3_config():
    # ensure .env is setup properly
    bucket = getenv("AWS_BUCKET_NAME")
    if not bucket:
        raise RuntimeError(f"AWS_BUCKET_NAME is not set")
    access_key = getenv("AWS_ACCESS_KEY")
    if not access_key:
        raise RuntimeError(f"AWS_ACCESS_KEY is not set")
    secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
    if not secret_access_key:
        raise RuntimeError(f"AWS_SECRET_ACCESS_KEY is not set")
    return bucket, access_key, secret_access_key


bucket, access_key, secret_access_key = get_s3_config()
s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key,
)


def handle_upload(image, image_url: str):
    img_bytes = image.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        res, msg = upload_file(tmp_file.name, image_url)
        if not res:
            return (False, msg)
    return (True, msg)


def upload_file(file_name, object_name):
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return (False, e)
    return (True, object_name)


def get_object_name(prefix: str, player_id: str, session_id: int):
    return f"{prefix}_{player_id}_{session_id}"
