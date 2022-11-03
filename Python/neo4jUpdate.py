import neo4j
import pymongo
from pymongo import MongoClient
import time

neo4j.ConnectNeo4J()

client = MongoClient("mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin")
logs = client['logs']
counters = logs['counter']
neo = logs['neo']

def update_neo4j(doc):
    CRUD = doc['command']
    Class = doc['className']
    obj = doc['classObject']
    if CRUD == 'CREATE':
        if Class == "User":
            neo4j.Create_User(obj['name'], obj['username'], obj['password'], obj['birthday'])
            counters.update_one({'_id':'neo'},{"$set":{'last_updated':doc['_id']}})
        if Class == "Bet":
            neo4j.Create_MoneyLine_Bet(obj['date'], obj['winner'], obj['amount'], obj['user'], obj['game'])
            counters.update_one({'_id':'neo'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'UPDATE':
        if Class == "User":
            neo4j.Update_User(obj['name'], obj['username'], obj['password'], obj['birthday'])
            counters.update_one({'_id':'neo'},{"$set":{'last_updated':doc['_id']}})
    elif CRUD == 'DELETE':
        if Class == "User":
            neo4j.Delete_User(obj['username'])
            counters.update_one({'_id':'neo'},{"$set":{'last_updated':doc['_id']}})

while neo.find_one({'_id':{'$gt':counters.find_one({'_id':'neo'})['last_updated']}}) is not None:
    try:
        neo4j.CheckConnection()
    except:
        time.sleep(0.100)
        continue
    docs = neo.find({'_id':{'$gt':counters.find_one({'_id':'neo'})['last_updated']}}).sort('_id')
    for doc in docs:
        update_neo4j(doc)


with neo.watch(full_document="updateLookup") as stream:
    for change in stream:
        update_neo4j(change['full_document'])