from datetime import datetime
import pytz
from urllib.parse import urlencode
import json
import decimal
from boto3.dynamodb.conditions import Key
from backend.configs import TWEET_TABLE, MANAGER_TABLE, TWITTER_API

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
        'object_id': dict_obj['id_str'],
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    return new_dict


def format_tpy_dict(dict_obj):
    dict_obj = json.loads(dict_obj)
    new_dict = {}
    new_dict.update({
        'object_id': dict_obj['id_str'],
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    # for k, v in dict_obj.items():
    #     if is_null(v) or is_empty_str(v):
    #         new_dict.update({
    #             k: "<empty value>"
    #         })
    #     else:
    #         new_dict.update({
    #             k: v
    #         })
    return new_dict


def store_tpy_tweet_db(tweet):
    response = TWEET_TABLE.put_item(
        Item=format_tpy_dict(tweet),
        ReturnValues='ALL_OLD'
    )
    return response


def fetch_recent_tweets(token, count=10):
    cur_date = str(datetime.now().date())
    token_dict = {
        'q': token,
        'since': cur_date,
        'result_type': 'recent',
        'count': count

    }
    query_str = urlencode(token_dict)
    api_resp = TWITTER_API.GetSearch(
        raw_query=query_str
    )
    tweets = []
    for tweet in api_resp:
        tweets.append(tweet._json)
    return tweets


def store_tweet_db(tweet):
    TWEET_TABLE.put_item(
        Item=format_ptw_dict(tweet)
    )


def get_stream_status():
    response = MANAGER_TABLE.scan(
        FilterExpression=(
            Key('manager_id').eq(1)
        )
    )
    manager = response['Items'][0]
    return manager['stream_status']


def set_run_status():
    cur_ts = str(utc.localize(datetime.now()))
    MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression=('SET stream_status = :val1, '
                          'ts_start = :val2, cur_sqs_count = :val3, cur_insert_count = :val4'),
        ExpressionAttributeValues={
            ':val1': True,
            ':val2': cur_ts,
            ':val3': 0,
            ':val4': 0
        }
    )


def set_sqs_count():
    MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression='SET cur_sqs_count = cur_sqs_count + :val1,',
        ExpressionAttributeValues={
            ':val1': 1,
        }
    )


def set_insert_count():
    MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression='SET cur_insert_count = cur_insert_count + :val1,',
        ExpressionAttributeValues={
            ':val1': 1,
        }
    )


def set_stop_status():
    cur_ts = str(utc.localize(datetime.now()))
    MANAGER_TABLE.update_item(
        Key={
            'manager_id': 1,
        },
        UpdateExpression='SET stream_status = :val1, ts_end= :val2',
        ExpressionAttributeValues={
            ':val1': False,
            ':val2': cur_ts
        }
    )
