from datetime import datetime
import pytz
from backend.configs import SQS, SQS_QUEUE_URL
utc = pytz.utc


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

