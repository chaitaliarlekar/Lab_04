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
    db = client['analytics']
    for docs in db.analytics.customers.find({},{"username":1,"accounts":1}):
        count=0
        sumLimit=0
        flag=0
        for i in docs["accounts"]:
            for doc in db.analytics.accounts.find({"account_id":i, "products":"Commodity"}):
                count+=1
                flag=1
                sumLimit+=doc["limit"]
        if(flag==1):
            print("Average limit of account holder: ",docs["username"],"is: ",sumLimit/count)
  
    
finally:
	client.close()

