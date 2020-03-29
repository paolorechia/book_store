import json
import boto3

from lib import repository

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DevTable')


def test_lambda_handler(event, context):
    table.put_item(
        Item={
            'name': 'Novo',
            'author': 'NovoAutor'
        })
    response = table.get_item(
        Key={
            'name': 'O Hobbit',
            'author': 'J.R.R. Tolkien'
        }
    )
    print(response)
    item = response['Item']
    print(item)
    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": item,
        }),
    }


def put_item_handler(event, context):
    print(event)
    request_body = json.loads(event['body'])
    try:
        repository.put_item_into_table(table, request_body)
    except Exception as err:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Creation failed: {}".format(str(err)),
            }),
        }
    return {
        "statusCode": 201,
        "body": "Created\n"
    }
