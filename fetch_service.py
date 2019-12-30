from fetch_lib.helpers import process_record


def handler(event, context):
    print('Invoked fetch service!')
    for record in event['Records']:
        process_record(record)
    print('Fetch Finished!')
    return True
