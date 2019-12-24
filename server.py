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

    type Mutation {
        locationUpdate (_id: String!, name: String!): Location,
        locationCreate (name: String!): Location,
    }

    type Location {
        _id: String,
        name: String,
        test: String
    }


""")
location = ObjectType("Query")
mutation = ObjectType("Mutation")
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

@mutation.field("locationUpdate")
def resolve_location_update(_, info, _id=None, name=None):
    print('UPDATE Mutation!')
    fetched = book_db.location.find_one({"_id": ObjectId(_id)})
    fetched['name']=name
    u = book_db.location.update_one({"_id": ObjectId(_id)}, {"$set": fetched})
    if u.acknowledged:
        return fetched

@mutation.field("locationCreate")
def resolve_location_create(_, info, _id=None, name=None):
    print('Create Mutation!')
    c = book_db.location.insert_one({"name": name})
    return book_db.location.find_one({"_id": c.inserted_id})

schema = make_executable_schema(type_defs, [query, mutation])
app = GraphQL(schema, debug=True)
