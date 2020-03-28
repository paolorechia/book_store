#!/bin/bash


api_url=https://2md4993fw9.execute-api.us-east-1.amazonaws.com/Dev

curl -X GET -H "Authorization: $1" $api_url/hello

