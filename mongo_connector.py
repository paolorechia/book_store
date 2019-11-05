import sys

port='27017'
host='localhost'
user='root'
password='example'

database='book'

#mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[database][?options]]
from pymongo import MongoClient

sys.stdout.write('Connecting to Mongo database...')
sys.stdout.flush()
client = MongoClient( 'mongodb://{}:{}@{}:{}'\
    .format(user, password, host, port)
)
book_db = client.book
mongo_cursor  = book_db.test.find({})
for c in mongo_cursor:
    for k,v in c.items():
        continue

sys.stdout.write(' succedeed!\n')
sys.stdout.flush()
