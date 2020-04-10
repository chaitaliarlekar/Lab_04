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
    answer=0
    db = client['analytics']
    # write your code here
    for docs in db.analytics.customers.aggregate([{"$unwind":"$accounts"},{"$project":{"accounts":1,"name":1,"username":1}}]):
        if docs["name"]=="James Smith" and docs["username"]=="ashley97":
            for docs1 in db.analytics.transactions.aggregate([{"$unwind":"$transactions"},{"$match":{"account_id":docs["accounts"]}},{"$project":{"transactions.transaction_code":1,"transactions.total":1}}]):
                if docs1["transactions"]["transaction_code"]=="buy":
                    answer+=float(docs1["transactions"]["total"])
    print("Total Buy:",round(answer))
finally:
	client.close()

