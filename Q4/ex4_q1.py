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
    db = client['analytics']
    for docs in db.analytics.accounts.aggregate([{"$unwind":"$products"},{"$match":{"products":"InvestmentStock"}}]):
        for docs1 in db.analytics.customers.aggregate([{"$unwind":"$accounts"},{"$match":{"accounts":docs["account_id"]}},{"$project":{"accounts":1,"username":1,"name":1,"email":1}}]):
            pprint(docs1)
    
finally:
	client.close()

