import requests
from flask_restful import Resource
from flask import request
import backend.configs as configs
import backend.helpers as helpers


class Home(Resource):
    def get(self):
        return {'msg': 'Welcome Home!'}


class TweetList(Resource):
    def get(self):
        token = request.args.get('token', 'a')
        count = request.args.get('count', 10)
        tweets = helpers.get_stored_tweets(token=token, count=count)
        return {
            'tweets': tweets,
            'tweet_count': len(tweets)
        }


class StreamStart(Resource):
    def get(self):
        tokens = request.args.get('tokens', 'a;b')
        count = request.args.get('count', 100)
        if helpers.get_stream_status():
            return {'msg': 'Tweet Stream is already Started!'}, 406
        token_list = list(filter(None, tokens.split(';')))
        helpers.set_run_status()
        response = requests.get(
            configs.STREAM_URL,
            params={
                'token_list': token_list,
                'count': count
            }
        )
        if response.status_code == 200:
            msg = {'msg': 'Tweet Stream Started!'}
        else:
            msg = {'msg': 'Stream error occurred!'}
        return msg


class StreamStop(Resource):
    def get(self):
        if not helpers.get_stream_status():
            return {'msg': 'Tweet Stream is not running!'}, 406
        helpers.set_stop_status()
        return {'msg': 'Tweet Stream Stopped!'}


class StreamConfigs(Resource):
    def get(self):
        return helpers.get_stream_configs()


class LiveTweets(Resource):
    def get(self):
        token = request.args.get('token', '')
        count = request.args.get('count', 10)
        tweets = helpers.get_live_tweets(token=token, count=count)
        return {'tweet_count': len(tweets), 'tweets': tweets}

