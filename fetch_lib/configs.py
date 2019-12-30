import os
import boto3


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DDB = boto3.resource('dynamodb')
TWEET_TABLE = DDB.Table('twitter_feed')
MANAGER_TABLE = DDB.Table('stream_manager')


