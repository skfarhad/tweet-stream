import json
from boto3.dynamodb.conditions import Key
from fetch_lib.configs import TWEET_TABLE


def store_sqs_record_db(sqs_record):
    dict_obj = json.loads(sqs_record)
    new_dict = {}
    new_dict.update({
        'object_id': dict_obj['id_str'],
        'created_at': dict_obj['created_at'],
        'text': dict_obj['text'],
        'body': json.dumps(dict_obj)
    })
    response = TWEET_TABLE.put_item(
        Item=new_dict,
        ReturnValues='ALL_OLD'
    )
    return response


def process_record(record):
    try:
        msg_body = record["body"]
        msg_id = record['messageId']
        store_sqs_record_db(msg_body)
        print('Stored message with id: ' + str(msg_id))
    except Exception as e:
        print('Exception in fetch: ' + str(e))

