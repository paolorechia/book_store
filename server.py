from flask import Flask, escape, request
from flask_restplus import Resource, Api, fields, abort
from marshmallow import Schema, fields as mfields, pprint
from marshmallow.exceptions import ValidationError
from datetime import datetime
from collections import namedtuple 
import os
from mongo_connector import client, book_db

app = Flask(__name__)
api = Api(app)

Location = namedtuple("Location", "id name")
locationModel = api.model('LocationModel', {
    'id': fields.Integer,
    'name': fields.String
})
class LocationSchema(Schema):
    id = mfields.Integer()
    name = mfields.Str()

Book = namedtuple("Book", "name author publication_date editor location leased")
bookModel = api.model('BookModel', {
    'name': fields.String,
    'author': fields.String,
    'publication_date': fields.DateTime,
    'editor': fields.String,
    'location': fields.String,
    'leased': fields.String
})

def mongo_cursor_to_list(mongo_cursor):
    entities = [] 
    for e in mongo_cursor:
       del e['_id']
       entities.append(e) 
    return entities

@api.route('/locations')
class LocationResource(Resource):
    @api.marshal_with(locationModel)
    def get(self):
        locations = mongo_cursor_to_list(book_db.location.find({}))
        return locations

    @api.expect(locationModel)
    def put(self):
        schema = LocationSchema()
        try:
            l = schema.load(request.json)
        except ValidationError as excp:
            print(excp)
            abort(400, excp)
        fetched= book_db.location.find_one({'id': l['id']})
        if fetched is None:
            abort(404, 'Not Found')
        book_db.location.update_one({'id': l['id']}, {'$set': l})
        return l

    @api.expect(locationModel)
    def post(self):
        schema = LocationSchema(exclude=["id"])
        try:
            l = schema.load(request.json)
        except ValidationError as excp:
            print(excp)
            abort(400, excp)
        book_db.location.insert_one(l)
        return l

@api.route('/locations/<id>')
class LocationResource(Resource):
    @api.marshal_with(locationModel)
    def get(self, id):
        id_ = int(id)
        location = book_db.location.find_one({'id': id_ })
        if location is None:
            abort(404, 'Location not found')
        return location

    def delete(self, id):
        return {'location': 'delete'}

@api.route('/books')
class BookResource(Resource):
    def get(self):
        return {'book': 'get'}
    def put(self):
        return {'book': 'put'}
    def post(self):
        return {'book': 'post'}
    def delete(self):
        return {'book': 'delete'}


if __name__ == "__main__":
    if os.getenv('FLASK_ENV') == 'development':
        debug = True
    else:
        debug = False
    app.run(host='0.0.0.0', port='4040', debug=debug)
