# AWS_SCHEMA
> dataclass for aws dictionaries


This library aims to parse aws dictionaries and json strings into dataclass objects

## Install

`pip install awsSchema`

## How to use

extract data from aws classes eg apigateway lambda input/output
this library uses jsondataclass, and dataclass

## API Gateway integration

```
from awsSchema.apigateway import Response, Event
```

## parsing event

```
dummyEvent =  { "resource": "/{proxy+}", "path": "/hello/world", "httpMethod": "POST", "headers": { "Accept": "*/*", "Accept-Encoding": "gzip, deflate", "cache-control": "no-cache", "CloudFront-Forwarded-Proto": "https", "CloudFront-Is-Desktop-Viewer": "true", "CloudFront-Is-Mobile-Viewer": "False", "CloudFront-Is-SmartTV-Viewer": "False", "CloudFront-Is-Tablet-Viewer": "False", "CloudFront-Viewer-Country": "US", "Content-Type": "application/json", "headerName": "headerValue", "Host": "gy415nuibc.execute-api.us-east-1.amazonaws.com", "Postman-Token": "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f", "User-Agent": "PostmanRuntime/2.4.5", "Via": "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)", "X-Amz-Cf-Id": "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==", "X-Forwarded-For": "54.240.196.186, 54.182.214.83", "X-Forwarded-Port": "443", "X-Forwarded-Proto": "https" }, "multiValueHeaders":{ 'Accept':[ "*/*" ], 'Accept-Encoding':[ "gzip, deflate" ], 'cache-control':[ "no-cache" ], 'CloudFront-Forwarded-Proto':[ "https" ], 'CloudFront-Is-Desktop-Viewer':[ "true" ], 'CloudFront-Is-Mobile-Viewer':[ "False" ], 'CloudFront-Is-SmartTV-Viewer':[ "False" ], 'CloudFront-Is-Tablet-Viewer':[ "False" ], 'CloudFront-Viewer-Country':[ "US" ], '':[ "" ], 'Content-Type':[ "application/json" ], 'headerName':[ "headerValue" ], 'Host':[ "gy415nuibc.execute-api.us-east-1.amazonaws.com" ], 'Postman-Token':[ "9f583ef0-ed83-4a38-aef3-eb9ce3f7a57f" ], 'User-Agent':[ "PostmanRuntime/2.4.5" ], 'Via':[ "1.1 d98420743a69852491bbdea73f7680bd.cloudfront.net (CloudFront)" ], 'X-Amz-Cf-Id':[ "pn-PWIJc6thYnZm5P0NMgOUglL1DYtl0gdeJky8tqsg8iS_sgsKD1A==" ], 'X-Forwarded-For':[ "54.240.196.186, 54.182.214.83" ], 'X-Forwarded-Port':[ "443" ], 'X-Forwarded-Proto':[ "https" ] }, "queryStringParameters": { "name": "me", "multivalueName": "me" }, "multiValueQueryStringParameters":{ "name":[ "me" ], "multivalueName":[ "you", "me" ] }, "pathParameters": { "proxy": "hello/world" }, "stageVariables": { "stageVariableName": "stageVariableValue" }, "requestContext": { "accountId": "12345678912", "resourceId": "roq9wj", "stage": "testStage", "requestId": "deef4878-7910-11e6-8f14-25afc3e9ae33", "identity": { "cognitoIdentityPoolId": None, "accountId": None, "cognitoIdentityId": None, "caller": None, "apiKey": None, "sourceIp": "192.168.196.186", "cognitoAuthenticationType": None, "cognitoAuthenticationProvider": None, "userArn": None, "userAgent": "PostmanRuntime/2.4.5", "user": None }, "resourcePath": "/{proxy+}", "httpMethod": "POST", "apiId": "gy415nuibc" }, "body": "{\r\n\t\"a\": 1\r\n}", "isBase64Encoded": False }
event = Event.from_dict(dummyEvent)
type(event)
```




    awsSchema.apigateway.Event



### parsing for body

```
Event.parseBody(dummyEvent)
```




    {'a': 1}



## creating response for apiGateway

```
print(Response.returnSuccess(body={'hello':'world'}))
print(Response.returnError(message='error'))
```

    {'body': '{"hello":"world"}', 'statusCode': 200, 'headers': {}}
    {'body': '{"error":"error"}', 'statusCode': 400, 'headers': {}}


## Use in lambda function

```
def lambda_handler(event, *args):
  # parsing event body
  body = Event.parseBody(event)
  
  
  # submitting output
  return Response.returnSuccess(body = {'success':'true'})

lambda_handler(dummyEvent)
```




    {'body': '{"success":"true"}', 'statusCode': 200, 'headers': {}}



## getting around lambda proxy integration for sdk

```
#trigger lambda
inputBody = {'test':'123'}

inputToFunction = Event.getInput(body = inputBody) ; print(f'inputToFunction is {inputToFunction}')
response = lambda_handler(inputToFunction); print(f'rawResponse is {response}')
parsedResponse = Response.parseBody(response); print(f'parsedResponse is {parsedResponse}')
```

    inputToFunction is {'body': '{"test":"123"}', 'headers': {}, 'statusCode': 200}
    rawResponse is {'body': '{"success":"true"}', 'statusCode': 200, 'headers': {}}
    parsedResponse is {'success': 'true'}


## S3

```
from awsSchema.S3 import S3Event
```

```
# test get key object
eventSample = { "Records": [ { "eventVersion": "2.1", "eventSource": "aws:s3", "awsRegion": "us-east-2", "eventTime": "2019-09-03T19:37:27.192Z", "eventName": "ObjectCreated:Put", "userIdentity": { "principalId": "AWS:AIDAINPONIXQXHT3IKHL2" }, "requestParameters": { "sourceIPAddress": "205.255.255.255" }, "responseElements": { "x-amz-request-id": "D82B88E5F771F645", "x-amz-id-2": "vlR7PnpV2Ce81l0PRw6jlUpck7Jo5ZsQjryTjKlc5aLWGVHPZLj5NeC6qMa0emYBDXOo6QBU0Wo=" }, "s3": { "s3SchemaVersion": "1.0", "configurationId": "828aa6fc-f7b5-4305-8584-487c791949c1", "bucket": { "name": "bucketname", "ownerIdentity": { "principalId": "A3I5XTEXAMAI3E" }, "arn": "arn:aws:s3:::lambda-artifacts-eafc19498e3f2df" }, "object": { "key": "theKey", "size": 1305107, "eTag": "b21b84d653bb07b05b1e6b33684dc11b", "sequencer": "0C0F6F405D6ED209E1" } } } ] }
bucket, key = S3Event.getKeyObject(eventSample)
print(bucket,key)
```

    bucketname theKey


## Parsing data class directly

```
from dataclasses import field
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined
@dataclass_json
@dataclass
class Product:
  cprcode: str
  iprcode: str
  oprcode: str
  ordertype: str
  pr_abb: str
    
productDict = Product(
  cprcode='123',
  iprcode='123',
  oprcode= '12343',
  ordertype='3225',
  pr_abb='4563'
).to_dict()
productDict
```




    {'cprcode': '123',
     'iprcode': '123',
     'oprcode': '12343',
     'ordertype': '3225',
     'pr_abb': '4563'}



```
event = Event.getInput(productDict)
Event.parseDataClass(Product, event)
```




    Product(cprcode='123', iprcode='123', oprcode='12343', ordertype='3225', pr_abb='4563')


