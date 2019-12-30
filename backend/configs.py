import os
import json
import boto3
import twitter


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DDB = boto3.resource('dynamodb')
TWEET_TABLE = DDB.Table('tweets')
MANAGER_TABLE = DDB.Table('stream_manager')
SQS = boto3.client('sqs')
STREAM_URL = 'https://fe2h7ne666.execute-api.us-west-2.amazonaws.com/default/tweet_streamer'

with open(os.path.join(BASE_DIR, 'credentials.json')) as config_file:
    CONFIG = json.load(config_file)

SQS_QUEUE_URL = CONFIG['SQS_QUEUE_URL']

TWITTER_API = twitter.Api(
    consumer_key=CONFIG['consumer_key'],
    consumer_secret=CONFIG['consumer_secret'],
    access_token_key=CONFIG['access_token_key'],
    access_token_secret=CONFIG['access_token_secret']
)
