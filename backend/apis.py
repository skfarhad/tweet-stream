from flask_restful import Resource
from flask import request
from boto3.dynamodb.conditions import Key, Attr
from app_apis.configs import FEED_TABLE, MANAGER_TABLE
from app_apis.helpers import get_stream_status, set_run_status, set_stop_status, \
    get_json, fetch_recent_tweets, store_tweet_db


class Home(Resource):
    def get(self):
        return {'msg': 'Welcome Home!'}


class TweetList(Resource):
    def get(self):
        token = request.args.get('token', 'a')
        count = request.args.get('count', 10)
        response = FEED_TABLE.scan(
            FilterExpression=(
                Attr('object_id').ne('None') &
                Attr('text').contains(token)
            ),
            Limit=int(count)
        )
        items = response['Items']
        tweets = []
        for tweet in items:
            tweets.append(get_json(tweet))

        return tweets


class StreamStart(Resource):
    def post(self):
        tokens = request.form.get('tokens', '')
        if get_stream_status():
            return {'msg': 'Tweet Stream is already Started!'}, 406
        token_list = list(filter(None, tokens.split(';')))
        set_run_status()
        return {'msg': 'Tweet Stream Started!'}


class StreamStop(Resource):
    def post(self):
        if not get_stream_status():
            return {'msg': 'Tweet Stream is not running!'}, 406
        set_stop_status()
        return {'msg': 'Tweet Stream Stopped!'}


class StreamStatusDetails(Resource):
    def get(self):
        response = MANAGER_TABLE.scan(
            FilterExpression=(
                Key('manager_id').eq(1)
            )
        )
        manager = response['Items'][0]
        return get_json(manager)


class FetchNewTweets(Resource):
    def get(self):
        token = request.args.get('token', '')
        count = request.args.get('count', 10)
        tweets = fetch_recent_tweets(token=token, count=count)
        return {'tweet_count': len(tweets), 'tweets': tweets}

    def post(self):
        token = request.args.get('token', '')
        count = request.args.get('count', 10)
        tweets = fetch_recent_tweets(token=token, count=count)
        errors = []
        for tweet in tweets:
            try:
                store_tweet_db(tweet=tweet)
            except Exception as e:
                errors.append(str(e))
        return {'tweet_count': len(tweets), 'err_list': errors, 'error_count': len(errors)}
