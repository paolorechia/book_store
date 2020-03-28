#!/bin/bash

client_id=REPLACE
client_secret=REPLACE
basic_auth=$(printf $client_id:$client_secret | base64 - )
url=https://test-321.auth.us-east-1.amazoncognito.com/oauth2/token
curl -X POST -H "Authorization:Basic $basic_auth" $url -d "grant_type=client_credentials" --dump-header u && cat u
