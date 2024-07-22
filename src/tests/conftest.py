import os
import boto3
from moto import mock_aws
import pytest

from varfish_installer.config import VARFISH_S3_BUCKET, VARFISH_S3_ENDPOINT_URL


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def aws(aws_credentials):
    _ = aws_credentials
    with mock_aws():
        yield boto3.client(
            "s3",
            endpoint_url=VARFISH_S3_ENDPOINT_URL,
            verify=True,
        )


@pytest.fixture
def create_bucket(aws):
    _ = aws
    boto3.client("s3").create_bucket(Bucket=VARFISH_S3_BUCKET)
