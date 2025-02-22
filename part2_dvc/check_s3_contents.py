import os

import boto3
from dotenv import load_dotenv


def get_session_student():
    load_dotenv()

    session = boto3.session.Session()

    return session.client(
        service_name="s3",
        endpoint_url="https://storage.yandexcloud.net",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID_STUDENT"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY_STUDENT"),
    )


if __name__ == "__main__":
    s3 = get_session_student()
    bucket_name = os.environ.get("S3_BUCKET_NAME")

    if s3.list_objects(Bucket=bucket_name).get("Contents"):
        for key in s3.list_objects(Bucket=bucket_name)["Contents"]:
            print(key["Key"])
