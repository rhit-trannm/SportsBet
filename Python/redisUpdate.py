import Redis
import pymongo
from pymongo import MongoClient
import time

Redis.ConnectRedis()

client = MongoClient("mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin")
logs = client['logs']
counters = logs['counter']
redis = logs['redis']

def update_redis(doc):
    CRUD = doc['command']
    Class = doc['className']
    User = doc['classObject']
    if CRUD == 'CREATE':
        if Class == "User":
            Redis.CreateUser(User['name'], User['username'], User['password'], User['birthday'])
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'UPDATE':
        if Class == "User":
            Redis.UpdateUser(User['name'], User['username'], User['password'], User['birthday'])
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'DELETE':
        if Class == "User":
            Redis.DeleteUser(User['username'])
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})

while redis.find_one({'_id':{'$gt':counters.find_one({'_id':'redis'})['last_updated']}}) is not None:
    try:
        Redis.Ping()
    except:
        time.sleep(0.100)
        continue
    docs = redis.find({'_id':{'$gt':counters.find_one({'_id':'redis'})['last_updated']}}).sort('_id')
    for doc in docs:
        update_redis(doc)


with redis.watch(full_document="updateLookup") as stream:
    for change in stream:
        update_redis(change['fullDocument'])