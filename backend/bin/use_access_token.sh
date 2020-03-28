#!/bin/bash


api_url=https://2md4993fw9.execute-api.us-east-1.amazonaws.com/Dev/hello/
access_token=

curl -X GET -H "Authorization: $access_token" $api_url/hello

