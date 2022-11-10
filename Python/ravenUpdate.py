import json
from types import SimpleNamespace

import RavenDB
import pymongo
from pymongo import MongoClient
import time

client = MongoClient(
    "mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin")
logs = client['logs']
counters = logs['counter']
raven = logs['raven']


def update_raven(doc):
    CRUD = doc['command']
    Class = doc['className']
    obj = doc['classObject']
    #obj = json.loads(json.dumps(obj), object_hook=lambda d: SimpleNamespace(**d))
    if CRUD == 'CREATE':
        if Class == "User":
            RavenDB.CreateUser(name=obj.get('name'), username=obj.get('username'), password=obj.get('password'),
                               birthday=obj.get('birthday'))
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Player":
            RavenDB.StorePlayer(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Team":
            RavenDB.StoreTeam(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Match":
            RavenDB.CreateMatch(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Bet":
            RavenDB.CreateBet(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "PlayerGame":
            object = RavenDB.PlayerGame(obj['PLAYER_ID'], obj['GAME_ID'], obj['GAME_DATE'],
            obj['MATCHUP'], obj['WL'], obj['MIN'], obj['FGM'], obj['FGA'], obj['FG_PCT'], obj['FG3M'],
            obj['FG3A'], obj['FG3_PCT'], obj['FTM'], obj['FTA'], obj['FT_PCT'], obj['OREB'], obj['DREB'],
            obj['REB'], obj['AST'], obj['STL'], obj['BLK'], obj['TOV'], obj['PF'], obj['PTS'], obj['PLUS_MINUS'])
            RavenDB.StoreGame(object)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
    elif CRUD == 'UPDATE':
        if Class == "User":
            RavenDB.UpdateUser(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Player":
            RavenDB.EditPlayer(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Team":
            RavenDB.EditTeam(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Match":
            RavenDB.EditMatch(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
        elif Class == "Bet":
            RavenDB.EditBet(obj)
            counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
    elif CRUD == 'DELETE':
        RavenDB.DeleteDocument(obj)
        counters.update_one({'_id': 'raven'}, {"$set": {'last_updated': doc['_id']}})
while True:
    while raven.find_one({'_id': {'$gt': counters.find_one({'_id': 'raven'})['last_updated']}}) is not None:
        try:
            RavenDB.TestConnection()
        except:
            time.sleep(0.100)
            continue
        docs = raven.find({'_id': {'$gt': counters.find_one({'_id': 'raven'})['last_updated']}}).sort('_id')
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
