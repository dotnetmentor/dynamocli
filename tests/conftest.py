from moto import mock_aws
import pytest
import os
import boto3

from src.document_visualizer import DocumentVisualizer


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"


@pytest.fixture(scope='function')
def visualizer():
    yield DocumentVisualizer()


@pytest.fixture(scope='function')
def dynamodb(aws_credentials):
    with mock_aws():
        yield boto3.resource('dynamodb', region_name='eu-west-1')


@pytest.fixture(scope='function')
def client(aws_credentials):
    with mock_aws():
        yield boto3.client('dynamodb', region_name='eu-west-1')


@pytest.fixture(scope='function')
def table(dynamodb):
    yield dynamodb.create_table(
        TableName='test_table',
        KeySchema=[{'AttributeName': 'pk', 'KeyType': 'HASH'},
                   {'AttributeName': 'sk', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[
            {'AttributeName': 'pk', 'AttributeType': 'S'},
            {'AttributeName': 'sk', 'AttributeType': 'S'},
            {"AttributeName": "gsi1pk", "AttributeType": "S"},
            {"AttributeName": "gsi1sk", "AttributeType": "S"},
        ],
        GlobalSecondaryIndexes=[
            {"IndexName": "gsi1",
             "KeySchema": [
                 {"AttributeName": "gsi1pk", "KeyType": "HASH"},
                 {"AttributeName": "gsi1sk", "KeyType": "RANGE"}],
             "Projection":  {"ProjectionType": "ALL"},
             "ProvisionedThroughput": {'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )
