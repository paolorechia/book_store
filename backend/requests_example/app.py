import json
import requests


sample_url = "http://openlibrary.org/search.json\?author\=tolkien"


def lambda_handler(event, context):
    requests.get(sample_url)
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
