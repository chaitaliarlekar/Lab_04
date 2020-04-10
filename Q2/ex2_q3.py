#Recommended to use python try-except block to perform error handling.
from pprint import pprint 
#use pprint instead of print to clearly print output documents
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure,OperationFailure
connectionString='mongodb+srv://201701101:201701101@mycluster-yony7.mongodb.net/test?retryWrites=true&w=majority'
#enter your connection String here
client=MongoClient(connectionString)

try:
    client.admin.command('ismaster')

except ConnectionFailure:
    print('Server not available')
    
except OperationFailure:
    print('wrong credentials')
    
else:
    print('connected to database')
    db = client['201701101']
    for docs in db.sales.aggregate([{"$unwind": { "path": "$items" }   },{"$group":{"_id": "$storeLocation", "totalSales":{"$sum": {"$multiply":["$items.price","$items.quantity"]}}}}]):
        pprint(docs)
    for docs in db.sales.aggregate([{"$group":{"_id":"$storeLocation","totalTransaction":{"$sum":1}}}]):
        pprint(docs)
    
finally:
	client.close()
