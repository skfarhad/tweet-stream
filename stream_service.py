# -*- coding: utf-8 -*-

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from app_configs import CONFIG
from app_helpers import get_stream_status, set_stop_status, store_tpy_tweet_db

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
            store_tpy_tweet_db(data)
            # print('Uploaded data..')
        except Exception as e:
            pass
            # print(str(e))
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
