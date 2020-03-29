import json
import boto3

from libs import repository

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
    request_body = json.loads(event['body'])
    print(request_body)
    context = repository.put_context()
    print("Entering context")
    with context:
        repository.put_item_into_table(table, request_body)
    print("Exited context")
    print(context.response)
    return context.response
