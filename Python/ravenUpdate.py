import RavenDB
import pymongo
from pymongo import MongoClient
import time

client = MongoClient("mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin")
logs = client['logs']
counters = logs['counter']
raven = logs['raven']

def update_raven(doc):
    CRUD = doc['command']
    Class = doc['className']
    obj = doc['classObject']
    if CRUD == 'CREATE':
        if Class == "User":
            RavenDB.CreateUser(name=obj['name'], username=obj['username'], password=obj['password'], birthday=obj['birthday'])
            counters.update_one({'_id':'raven'},{"$set":{'last_updated':doc['_id']}})
        elif Class == "Player":
            RavenDB.StorePlayer(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Team":
            RavenDB.StoreTeam(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
            print('x')
        elif Class == "Match":
            print('x')
        elif Class == "Bet":
            print('x')

    elif CRUD == 'UPDATE':
        if Class == "User":
            RavenDB.UpdateUser(obj['name'], obj['username'], obj['password'], obj['birthday'])
            counters.update_one({'_id':'raven'},{"$set":{'last_updated':doc['_id']}})
        elif Class == "Player":
            print('x')
        elif Class == "Team":
            print('x')
        elif Class == "Match":
            print('x')
        elif Class == "Bet":
            print('x')
    elif CRUD == 'DELETE':
        if Class == "User":
            RavenDB.DeleteUser(obj['username'])
            counters.update_one({'_id':'raven'},{"$set":{'last_updated':doc['_id']}})
        elif Class == "Player":
            print('x')
        elif Class == "Team":
            print('x')
        elif Class == "Match":
            print('x')
        elif Class == "Bet":
            print('x')

while True:
    while raven.find_one({'_id':{'$gt':counters.find_one({'_id':'raven'})['last_updated']}}) is not None:
        try:
            RavenDB.TestConnection()
        except:
            time.sleep(0.100)
            continue
        docs = raven.find({'_id':{'$gt':counters.find_one({'_id':'raven'})['last_updated']}}).sort('_id')
        for doc in docs:
            try:
                RavenDB.TestConnection()
            except:
                break
            update_raven(doc)


    with raven.watch(full_document="updateLookup") as stream:
        for change in stream:
            try:
                RavenDB.TestConnection()
            except:
                break
            update_raven(change['fullDocument'])