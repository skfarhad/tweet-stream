from datetime import datetime
import pytz
import json
from boto3.dynamodb.conditions import Key
from stream_lib.configs import MANAGER_TABLE
from stream_lib.configs import SQS, SQS_QUEUE_URL

utc = pytz.utc


def format_tpy_dict(dict_obj):
    dict_obj = json.loads(dict_obj)
    new_dict = {}
    new_dict.update({
        'object_id': dict_obj['id_str'],
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    return new_dict


def get_stream_status():
    response = MANAGER_TABLE.scan(
        FilterExpression=(
            Key('manager_id').eq(1)
        )
    )
    manager = response['Items'][0]
    return manager['stream_status']


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


def send_message(msg_str, object_id, count=0):
    cur_ts = str(utc.localize(datetime.now()))
    response = SQS.send_message(
        QueueUrl=SQS_QUEUE_URL,
        DelaySeconds=10,
        MessageAttributes={
            'Timestamp': {
                'DataType': 'String',
                'StringValue': cur_ts
            },
            'Count': {
                'DataType': 'String',
                'StringValue': str(count)
            },
            'ObjectId': {
                'DataType': 'Number',
                'StringValue': object_id
            }
        },
        MessageBody=msg_str
    )
    # print(response['MessageId'])
    return response['MessageId']
