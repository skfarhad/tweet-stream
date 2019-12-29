# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from backend.configs import CONFIG
from backend.helpers import get_stream_status, \
    set_stop_status, format_tpy_dict, set_sqs_count
from stream_utils import send_message

consumer_key = CONFIG['consumer_key']
consumer_secret = CONFIG['consumer_secret']
access_token_key = CONFIG['access_token_key']
access_token_secret = CONFIG['access_token_secret']


class TweetStreamListener(StreamListener):

    def on_data(self, data):
        # TODO: Push to SQS
        if not get_stream_status():
            set_stop_status()
            # print('Stopping stream..')
            return False
        try:
            msg_obj = format_tpy_dict(data)
            msg_id = send_message(msg_str=msg_obj['body'], object_id=msg_obj['object_id'])
            set_sqs_count()
            print('Sent message to sqs with id: ', msg_id)
        except Exception as e:
            pass
            # print('Exception in send message: ' + str(e))
            # set_stop_status()
            # return False

        return True

    def on_error(self, status):
        # print('Error status: ', status)
        set_stop_status()
        return False


def start_stream(token_list=None):
    listener = TweetStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=token_list, is_async=False)


def handler(event, context):
    # Your code goes here!
    token_list = event.get('token_list', ['python'])
    count = event.get('count', 1000)
    start_stream(token_list=token_list)
    return 'Stream Finished!'
