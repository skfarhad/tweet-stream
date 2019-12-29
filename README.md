#Tweet Streaming service

###User Guide:
The following API endpoints are provided for collecting and browsing Recent
tweets.

Tweets can be collected having specific keywords and hashtags.
<br>Streaming process can be started using '/stream/start?token=aws%20lambda' API. 
<br>This will collect tweets have the phrase 'aws lambda'. Streaming can be stopped using '/stream/stop' API.
<br>Stream status can be monitored using '/stream/status'.

<br>Collected topics can be browsed and analyzed later using the '/tweets' API.
<br>Tweets can be filter with 'token' query param like this- '/tweets?token=metoo'.
<br>Max number of tweets returned can be specified using 'count' query param like this- '/tweets?count=10'

###Service Architecture:
The API endpoints are implemented using Flask framework. It's hosted in AWS lambda.
<br>There two more lambda functions for fetching tweets from twitter real-time api and pushing into AWS SQS.
<br>Later, pushed messaged are extracted and stored in DynamoDB. Those functions are implemented in Python.

###Build Process
To deploy the Flask app to AWS Lambda, zappa was used. Deployment Process-
<br><code>
<br>zappa init
<br>zappa deploy dev
</code>

To deploy the python functions in Lambda, python-lambda tool was used. Process-
<br><code>
<br>lambda init
<br>lambda deploy-s3 --config-file stream_config.yaml
</code>