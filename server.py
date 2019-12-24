import json
import os
from collections import namedtuple
from datetime import datetime

from ariadne import QueryType, ObjectType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from ariadne.constants import PLAYGROUND_HTML

from mongo_connector import book_db, client
from bson.objectid import ObjectId

type_defs = gql("""
    type Query {
        hello: String!,
        location (_id: String, name: String): [Location!]!
    }

    type Location {
        _id: String,
        name: String,
        test: String
    }
""")
location = ObjectType("Query")
query = QueryType()

@query.field("location")
def resolve_location(_, info, _id=None, name=None):
    request = info.context["request"]
    print(request)
    user_agent = request.headers.get("user-agent", "guest")
    if _id is not None:
        locations = book_db.location.find({"_id": ObjectId(_id)})
    elif name is not None:
        locations = book_db.location.find({"name": name})
    else:   
        locations = book_db.location.find({})
    return locations

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
