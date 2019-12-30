from datetime import datetime
import time
import pytz
from urllib.parse import urlencode
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import backend.configs as configs

utc = pytz.utc


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


def get_json(obj):
    return json.loads(json.dumps(obj, cls=DecimalEncoder))


def format_ptw_dict(dict_obj):
    dict_obj = get_json(dict_obj)
    new_dict = {}
    new_dict.update({
        'object_id': int(time.time()*1000),
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    return new_dict


def get_stored_tweets(token='a', count=10):
    response = configs.TWEET_TABLE.scan(
        FilterExpression=(
                Attr('text').contains(token)
        ),
        Limit=int(count)
    )
    items = response['Items']
    tweets = []
    for tweet in items:
        tweets.append(json.loads(tweet['body']))
    return tweets


def get_live_tweets(token='a', count=10):
    cur_date = str(datetime.now().date())
    token_dict = {
        'q': token,
        'since': cur_date,
        'result_type': 'recent',
        'count': count

    }
    query_str = urlencode(token_dict)
    api_resp = configs.TWITTER_API.GetSearch(
        raw_query=query_str
    )
    tweets = []
    for tweet in api_resp:
        tweets.append(tweet._json)
    return tweets


def get_stream_configs():
    response = configs.MANAGER_TABLE.scan(
        FilterExpression=(
            Key('manager_id').eq(1)
        )
    )
    details = response['Items'][0]
    return get_json(details)


def get_stream_status():
    response = configs.MANAGER_TABLE.scan(
        FilterExpression=(
            Key('manager_id').eq(1)
        )
    )
    details = response['Items'][0]
    return details['stream_status']


def set_run_status(token_list='a;b'):
    cur_ts = str(utc.localize(datetime.now()))
    configs.MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression=(
            'SET stream_status = :val1,'
            'ts_start = :val2,'
            'cur_sqs_count = :val3,' 
            'cur_insert_count = :val4,'
            'token_list = :val5'
        ),
        ExpressionAttributeValues={
            ':val1': True,
            ':val2': cur_ts,
            ':val3': 0,
            ':val4': 0,
            ':val5': token_list
        }
    )


def set_stop_status():
    cur_ts = str(utc.localize(datetime.now()))
    configs.MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression='SET stream_status = :val1, ts_end= :val2',
        ExpressionAttributeValues={
            ':val1': False,
            ':val2': cur_ts
        }
    )


def storage_details():
    count = configs.TWEET_TABLE.item_count
    return {
        'table': 'tweets',
        'item_count': count
    }


def clean_storage():
    scan = configs.TWEET_TABLE.scan()
    with configs.TWEET_TABLE.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'object_id': each['object_id']
                }
            )
