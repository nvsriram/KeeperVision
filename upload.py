from os import getenv
import boto3
import tempfile
from botocore.exceptions import ClientError
from botocore.config import Config


def get_s3_config():
    # ensure .env is setup properly
    bucket = getenv("AWS_BUCKET_NAME")
    if not bucket:
        raise RuntimeError(f"AWS_BUCKET_NAME is not set")
    region = getenv("AWS_REGION")
    if not region:
        raise RuntimeError(f"AWS_REGION is not set")
    access_key = getenv("AWS_ACCESS_KEY")
    if not access_key:
        raise RuntimeError(f"AWS_ACCESS_KEY is not set")
    secret_access_key = getenv("AWS_SECRET_ACCESS_KEY")
    if not secret_access_key:
        raise RuntimeError(f"AWS_SECRET_ACCESS_KEY is not set")
    return bucket, region, access_key, secret_access_key


bucket, region, access_key, secret_access_key = get_s3_config()
s3_client = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_access_key,
    config=Config(region_name=region, signature_version="v4"),
)
expiration = 90 * 24 * 60  # 90 days


def handle_upload(image, image_url: str):
    img_bytes = image.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(img_bytes)
        res, msg = upload_file(tmp_file.name, image_url)
        if not res:
            return (False, msg)
        res, msg = create_presigned_url(image_url)
        if not res:
            return (False, msg)
    return (True, msg)


def upload_file(file_name, object_name):
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        return (False, e)
    return (True, object_name)


def create_presigned_url(object_name):
    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        return (False, e)
    return (True, presigned_url)


def get_object_name(prefix: str, player_id: str, session_id: int):
    return f"{prefix}_{player_id}_{session_id}"
