from flask import Flask, escape, request
from flask_restplus import Resource, Api, fields, abort

from marshmallow import Schema, fields as mfields, pprint
from marshmallow.exceptions import ValidationError

from datetime import datetime
from collections import namedtuple 
from bson.objectid import ObjectId
from bson import json_util

import os
import json

from mongo_connector import client, book_db

app = Flask(__name__)
api = Api(app)

Location = namedtuple("Location", "name")
locationModel = api.model('LocationModel', {
    '_id': fields.String,
    'name': fields.String
})
class LocationSchema(Schema):
    _id = mfields.Str()
    name = mfields.Str()

Book = namedtuple("Book", "name author publication_date editor location leased")
bookModel = api.model('BookModel', {
    '_id': fields.Integer,
    'name': fields.String,
    'author': fields.String,
    'publication_date': fields.DateTime,
    'editor': fields.String,
    'location': fields.String,
    'leased': fields.String
})
class BookSchema(Schema):
    _id = mfields.Str()
    name = mfields.String()
    author = mfields.String()
    publication_date = mfields.DateTime()
    editor = mfields.String()
    location = mfields.String()
    leased = mfields.String()

@api.route('/locations')
class LocationResource(Resource):
    @api.marshal_with(locationModel)
    def get(self):
        locations = [ e for e in (book_db.location.find({})) ]
        return locations

    @api.expect(locationModel)
    @api.marshal_with(locationModel)
    def put(self):
        schema = LocationSchema()
        try:
            l = schema.load(request.json)
        except ValidationError as excp:
            print(excp)
            abort(400, excp)

        _id = l['_id']
        del (l['_id'])

        fetched = book_db.location.find_one({"_id": ObjectId(_id)})

        if fetched is None:
            abort(404, 'Not Found')
        book_db.location.update_one({'_id': ObjectId(_id)}, {'$set': l})
        return l

    @api.expect(locationModel)
    @api.marshal_with(locationModel)
    def post(self):
        schema = LocationSchema(exclude=["_id"])
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
        location = book_db.location\
            .find_one({"_id": ObjectId(id)})
        if location is None:
            abort(404, 'Location not found')
        return location

    def delete(self, id):
        location = book_db.location\
            .find_one({"_id": ObjectId(id)})
        if location is None:
            abort(404, 'Location not found')
        book_db.location.delete_one({"_id": ObjectId(id)})
        return {'Successfully deleted _id': id}

@api.route('/books')
class BookResource(Resource):
    @api.marshal_with(bookModel)
    def get(self):
        books = [ e for e in (book_db.books.find({})) ]
        return books 

    @api.expect(bookModel)
    def put(self):
        return {'book': 'put'}

    @api.expect(bookModel)
    @api.expect(bookModel)
    def post(self):
        print(request.json)
        schema = BookSchema(exclude=["_id"])
        try:
            input_book = schema.load(request.json)
        except ValidationError as excp:
            print(excp)
            abort(400, excp)
        print(input_book)
        input_book['publication_date'] = input_book['publication_date'].timestamp()
        book_db.book.insert_one(input_book)
        input_book['_id'] = str(input_book['_id'])
        print(input_book)
        return input_book 

    def delete(self, id):
        book_db.book.delete_one({"_id": ObjectId(id)})
        return {'Successfully deleted _id': id}


if __name__ == "__main__":
    if os.getenv('FLASK_ENV') == 'development':
        debug = True
    else:
        debug = False
    app.run(host='0.0.0.0', port='4040', debug=debug)
