import os
import json
import boto3

from backend import repository

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def create_book_handler(event, context):
    print(event)
    if "body" not in event:
        raise Exception("Missing body")
    request_body = json.loads(event["body"])
    print(request_body)
    context = repository.put_context()
    print("Entering context")
    with context:
        repository.put_item_into_table(table, request_body)
    print("Exited context")
    print(context.response)
    return context.response


def get_books_handler(event, context):
    result = table.scan()
    books = []
    for item in result["Items"]:
        books .append({
            "name": item["name"],
            "author": item["author"],
        })
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps(books)
    }
    return response
    
