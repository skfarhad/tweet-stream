from fetch_lib.helpers import process_record


def handler(event, context):
    for record in event['Records']:
        process_record(record)
    print('Fetch Finished!')
    return True
