import os
import json
import boto3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DDB = boto3.resource('dynamodb')
MANAGER_TABLE = DDB.Table('stream_manager')
SQS = boto3.client('sqs')

with open(os.path.join(BASE_DIR, 'credentials.json')) as config_file:
    CONFIG = json.load(config_file)

SQS_QUEUE_URL = CONFIG['SQS_QUEUE_URL']

