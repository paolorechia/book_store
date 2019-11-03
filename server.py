from flask import Flask, escape, request, abort
from flask_restplus import Resource, Api
from datetime import datetime
from collections import namedtuple 
import os
from mongo_connector import client, book_db

app = Flask(__name__)
api = Api(app)

Location = namedtuple("Location", "id name")
Book = namedtuple("Book", "name author publication_date datetime editor location leased")

#class BookMongo(Object):

def mongo_cursor_to_list(mongo_cursor):
    entities = [] 
    for e in mongo_cursor:
       del e['_id']
       entities.append(e) 
    return entities

def mongo_cursor_fetchone(mongo_cursor):
    try:
        entity = next(mongo_cursor)
        del entity['_id']
        return entity
    except StopIteration:
        return None

@api.route('/locations')
class LocationResource(Resource):
    def get(self):
        locations = mongo_cursor_to_list(book_db.location.find({}))
        return locations
    def put(self):
        return {'location': 'put'}
    def post(self):
        return {'location': 'post'}

@api.route('/locations/<id>')
class LocationResource(Resource):
    def get(self, id):
        id_ = int(id)
        cursor = book_db.location.find({'id': id_ })
        location = mongo_cursor_fetchone(cursor)
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
