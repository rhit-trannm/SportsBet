import json
from types import SimpleNamespace

import Redis
import pymongo
from pymongo import MongoClient
import time

Redis.ConnectRedis()

client = MongoClient("mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin")
logs = client['logs']
counters = logs['counter']
redis = logs['redis']


#Function for updating in redis using the document
def update_redis(doc):
    CRUD = doc['command']
    Class = doc['className']
    User = doc['classObject']
    #Checking CRUD type
    if CRUD == 'CREATE':
        #Checking class type - users are the only thing stored in redis.
        if Class == "User":
            #Calling Command from Redis.py file
            Redis.CreateUser(User['name'], User['username'], User['password'], User['birthday'])
            #Update the last_updated value for redis
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'UPDATE':
        if Class == "User":
            Redis.UpdateUser(User['name'], User['username'], User['password'], User['birthday'])
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'DELETE':
        if Class == "User":
            Redis.DeleteUser(User['username'])
            counters.update_one({'_id':'redis'},{"$set":{'last_updated':doc['_id']}})

while True:
#On initial startup, make sure there are no new logs since the last update
    while redis.find_one({'_id':{'$gt':counters.find_one({'_id':'redis'})['last_updated']}}) is not None:
        #Try pinging redis
        try:
            Redis.Ping()
        except:
            #Wait for 100 ms then try again
            time.sleep(0.100)
            continue

        #Get all new documents
        docs = redis.find({'_id':{'$gt':counters.find_one({'_id':'redis'})['last_updated']}}).sort('_id')
        #update for each doc
        for doc in docs:
            try:
                Redis.Ping()
            except:
                #break and go back to the top and wait
                break
            update_redis(doc)


    #Watch the redis collection for updates and react when they arrive
    with redis.watch(full_document="updateLookup") as stream:
        #Iteration for every change detected
        for change in stream:
            #Try pinging redis
            try:
                Redis.Ping()
            except:
                #break and go back to the top and wait
                break
            #Updating using the document that was changed
            update_redis(change['fullDocument'])