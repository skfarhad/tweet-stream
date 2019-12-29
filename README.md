# Tweet Streaming service
Service base endpoint: http://tweet.stream.skfarhad.com
### User Guide:
The following API endpoints are provided for collecting and browsing Recent
tweets.

Tweets can be collected having specific keywords and hashtags.
<br>Streaming process can be started using <code>'/stream/start?token=aws%20lambda'</code> API. 
<br>This request will start the stream process to collect the tweets with the phrase 'aws lambda'. 
<br>Streaming can be stopped using <code>'/stream/stop'</code> API.
<br>Status of streaming process can be monitored using <code>'/stream/status'</code>.

<br>Collected topics can be browsed and analyzed later using the <code>'/tweets'</code> API.
<br>Tweets can be filter with 'token' query param like this- <code>'/tweets?token=metoo'</code>.
<br>Max number of tweets returned can be specified using 'count' query param like this- <code>'/tweets?count=10'</code>

### Service Architecture:
The API endpoints are implemented using Flask framework. It's hosted in AWS lambda.
<br>There two more lambda functions for fetching tweets from twitter real-time api and pushing into AWS SQS.
<br>Later, pushed messaged are extracted and stored in DynamoDB. Those functions are implemented in Python.

### Build Process
To deploy the Flask app to AWS Lambda, [zappa](https://github.com/Miserlou/Zappa) was used. Deployment Process-
<br><code>
<br>zappa init
<br>zappa deploy dev
</code>

To deploy the python functions in Lambda, [python-lambda](https://github.com/nficano/python-lambda) tool was used. Process-
<br><code>
<br>lambda init
<br>lambda deploy-s3 --config-file stream_config.yaml
</code>
