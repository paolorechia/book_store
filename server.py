import json
import os
from collections import namedtuple
from datetime import datetime

from ariadne import QueryType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML

from mongo_connector import book_db, client

type_defs = gql("""
    type Query {
        hello: String!,
        location: [Location!]!
    }

    type Location {
        _id: String,
        name: String,
        test: String
    }
""")

query = QueryType()

@query.field("location")
def resolve_location(_, info):
    request = info.context["request"]
    print(request)
    user_agent = request.headers.get("user-agent", "guest")
    locations = book_db.location.find({})
    return locations

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)

