import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(
        TableName='DevTable',
        Item={
            'name': 'Test',
            'author': 'TestAuthor'
        })
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello dynamo",
        }),
    }
