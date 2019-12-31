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

<br>Collected tweets can be browsed and analyzed later using the <code>'/tweets'</code> API.
<br>Tweets can be filter with 'token' query param like this- <code>'/tweets?token=metoo'</code>.
<br>Max number of tweets returned can be specified using 'count' query param 
like this- <code>'/tweets?count=10'</code>

### Service Architecture:
The API endpoints are implemented using Flask framework. 
It's hosted in AWS Lambda using zappa.
<br>There are two more lambda functions. 
<br>One fetches the tweets from twitter real-time api and pushes those into SQS Queue. 
It's handler is located in <code>stream_service.py</code> file.
<br>The other one is used to extract SQS message from Queue and store in DynamoDB. It's details can be found in 
<code>fetch_service.py</code> file.
<br>Those functions are implemented in pure Python.

<br>Asynchronous API Gateway trigger is being used to trigger stream start service.
<br>The function checks if the stream status is true or not. 
<br>If true then it keeps fetching the tweets for 240 seconds which is set as timeout limit.

<br>If the user sets the status to false then the stream is stopped immediately.
<br>The SQS New Message event is used to trigger the function which store the tweets from SQS to DynamoDB. 

### Build Process
To deploy the Flask app to AWS Lambda, [zappa](https://github.com/Miserlou/Zappa) was used. 
Deployment Process-
<p>
<code>zappa init</code><br/>
<code>zappa deploy dev</code>
</p>

To deploy the python functions in Lambda, 
[python-lambda](https://github.com/nficano/python-lambda) tool was used. Process-
<p>
<code>lambda init</code><br/>
<code>lambda deploy-s3 --config-file stream_config.yaml
</code>
</p>
