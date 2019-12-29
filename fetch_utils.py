from backend.configs import SQS_QUEUE_URL, SQS
from backend.helpers import store_tpy_tweet_db, set_insert_count


def receive_message():
    # Receive message from SQS queue
    response = SQS.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        AttributeNames=[
            'Timestamp', 'Count', 'ObjectId'
        ],
        MaxNumberOfMessages=10,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )

    messages = response.get('Messages', [])
    for message in messages:
        msg_body = message['Body']
        msg_id = message['MessageId']
        receipt_handle = message['ReceiptHandle']
        # print(message)
        response = store_tpy_tweet_db(msg_body)
        if not response:
            set_insert_count()
        SQS.delete_message(
            QueueUrl=SQS_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        print('Stored message with id: %s', str(msg_id))
