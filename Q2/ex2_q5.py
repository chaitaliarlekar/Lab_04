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
    # write your code here
    db = client['201701101']
    pipeline=[]
    pipeline.append({'$unwind':'$items'})
    pipeline.append({'$group':{'_id':{'item_name':'$items.name','storeLocation':'$storeLocation'},'sales':{'$sum':'$items.quantity'}}})
    pipeline.append({'$group':{'_id':'$_id.item_name','sales_history':{'$addToSet':{'storeLocation':'$_id.storeLocation','quantity':'$sales'}}}})
    db.sales_replenish.insert_many(db.sales.aggregate(pipeline))
    
finally:
	client.close()
