import json
import time
from boto3.dynamodb.conditions import Key
from fetch_lib.configs import TWEET_TABLE, MANAGER_TABLE


def store_sqs_record_db(sqs_record):
    dict_obj = json.loads(sqs_record)
    new_dict = {}
    new_dict.update({
        'object_id': int(time.time()*1000),
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    response = TWEET_TABLE.put_item(
        Item=new_dict,
        ReturnValues='ALL_OLD'
    )
    if not response:
        set_insert_count()
    return response


def process_record(record):
    try:
        msg_body = record["body"]
        msg_id = record['messageId']
        store_sqs_record_db(msg_body)
        print('Stored message with id: ' + str(msg_id))
    except Exception as e:
        print('Exception in fetch: ' + str(e))


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


