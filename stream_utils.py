from datetime import datetime
import pytz
from boto3.dynamodb.conditions import Key, Attr
from app_configs import SQS, SQS_QUEUE_URL
utc = pytz.utc


def send_message(msg_str, count, object_id):
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

