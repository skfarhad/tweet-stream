from flask import Flask
from flask_restful import Api
from backend import apis

app = Flask(__name__)
api = Api(app)

api.add_resource(apis.Home, '/')
api.add_resource(apis.TweetList, '/tweets')
api.add_resource(apis.LiveTweets, '/tweets/live')

api.add_resource(apis.StreamStart, '/stream/start')
api.add_resource(apis.StreamStop, '/stream/stop')
api.add_resource(apis.StreamConfigs, '/stream/status')


if __name__ == '__main__':
    app.run(debug=True)
