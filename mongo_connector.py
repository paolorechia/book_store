port='27017'
host='localhost'
user='root'
password='example'

database='book'

#mongodb://[username:password@]host1[:port1][,...hostN[:portN]][/[database][?options]]
from pymongo import MongoClient

client = MongoClient( 'mongodb://{}:{}@{}:{}'\
    .format(user, password, host, port)
)

book_db = client.book
mongo_cursor  = book_db.test.find({})
for c in mongo_cursor:
    print(c)
    for k,v in c.items():
        print(k, v)
