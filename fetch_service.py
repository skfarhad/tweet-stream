# -*- coding: utf-8 -*-
from fetch_utils import receive_message


def handler(event, context):
    receive_message()
    return 'Fetch Finished!'
