import os
import json
import boto3

from backend import repository

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE"))


def put_item_handler(event, context):
    print(event)
    if "body" not in event:
        raise Exception("Missing body")
    request_body = event["body"]
    print(request_body)
    context = repository.put_context()
    print("Entering context")
    with context:
        repository.put_item_into_table(table, request_body)
    print("Exited context")
    print(context.response)
    return context.response
