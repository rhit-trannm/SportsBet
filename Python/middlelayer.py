import datetime

try:
    from Python import neo4j
    from Python import RavenDB
    from Python import Redis
except:
    import neo4j
    import RavenDB
    import Redis
from py2neo import Graph
from pyravendb.store import document_store
from types import SimpleNamespace
import json
import os
import pymongo
from pymongo import MongoClient
from pymongo import ReturnDocument


client = MongoClient("mongodb://logUser:abcd123@433-17.csse.rose-hulman.edu:27017,433-16.csse.rose-hulman.edu:27017,433-15.csse.rose-hulman.edu:27017/?replicaSet=rs0&authMechanism=DEFAULT&authSource=admin") 

db = client['logs']

counters = db['counter']

def get_id(db):
    new_id = counters.find_one_and_update({'_id':db}, {'$inc':{'last_written':1}}, return_document=ReturnDocument.AFTER)
    return new_id['last_written']



# Principles When coding middle layer:
# Read does not need to get written to file
# Write needs to get written to file

# routing logic: Ping each database before performing action. Check if they are up.
# Check if up to date,
# If it is not -> reroute and update it while rerouting.
# If it is -> Use database.

# User -> Duplicated on all 3 database. Should follow this roadmap... Redis -> Neo4j -> RavendB
# Bets -> Duplicated on Neo4J and RavenDB. Neo4J -> RavenDB.
# NBA Teams/Player info -> On RavenDB. Should never go down.

# In general, RavenDB should never go down. If it does go down, the entire system should go down.







class Friends(object):
    def __init__(self, user, friend):
        self.user = user
        self.friend = friend

class LogObject(object):
    def __init__(self, command, classObject, className):
        self.command = command
        self.classObject = classObject
        self.className = className

class Balance(object):
    def __init__(self, user, amount):
        self.user =user
        self.amount = amount


def Logging(CRUD, classObject):
    # Create log entry
    logEntry = LogObject(CRUD, classObject.__dict__, classObject.__class__.__name__).__dict__
    # Add to list of event
    if classObject.__class__.__name__ == "User": #go to all 3 databases
        logEntry['_id'] = get_id('redis')
        db.redis.insert_one(logEntry)
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "Balance":
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
    if classObject.__class__.__name__ == "Bet":
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
    if classObject.__class__.__name__ == "moneyLineBet":
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "overUnderBet":
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "Friends":
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "Match":
        # logEntry['_id'] = get_id('neo')
        # db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "Team":
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "PlayerGame":
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if classObject.__class__.__name__ == "TeamSeason":
        logEntry["_id"] = get_id('raven')
        db.raven.insert_one(logEntry)
    #NEED TO ADD FRIEND COMMANDS HERE EVENTUALLY

global UserCommands, BetCommands
Usercommands = ["Login"]
BetCommands = ["Cashout", "Check"]
def Routing(CRUD, object, command = None):
    if CRUD == "CREATE" or CRUD == "UPDATE" or CRUD == "DELETE":
        Logging(CRUD, object)
    elif CRUD == "READ": #Not stored in Mongo, rather is sent directly to databases
        #Need to check if each database is up to date according to logs.
        if object.__class__.__name__ == "User":
            if command == "Login":
                try:
                    if Redis.LoginCheck(object.username, object.password) == True:
                        print("OuterShellTrue1")
                        return True
                    else:
                        print("OuterShellFalse1")
                        return False
                except:
                    try:
                        if neo4j.Login_Check(object.username, object.password) == True:
                            print("OuterShellTrue2")
                            return True
                        else:
                            print("OuterShellFalse2")
                            return False
                    except:
                        try:
                            if RavenDB.LoginCheck(object.username, object.password) == True:
                                return True
                            else:
                                print("OuterShellFalse3")
                                return False
                        except:
                            print("All DB down")
                            return False
            elif command == "GetUser":
                try:
                    result = Redis.GetUser(username=object.username)
                    return result
                except:
                    try:
                        result = neo4j.GetUser(username=object.username)
                        return result
                    except:
                        try:
                            result = RavenDB.QueryUser(username=object.username)
                            return result
                        except:
                            print("All DB down")
                            return False
            elif command == "GetFriends":
                try:
                    result = neo4j.GetUser(username=object.username)
                    return result
                except:
                    try:
                        result = neo4j.GetUser(username=object.username)
                        return result
                    except:
                        try:
                            result = RavenDB.QueryUser(username=object.username)
                            return result
                        except:
                            print("All DB down")
                            return False

        elif object.__class__.__name__ == "Bet":
            if command == "GetBet":
                try:
                    result = neo4j.GetBet(object.betId)
                    return result
                except:
                    result = RavenDB.GetBet(object.betId)
                    return result
        elif object.__class__.__name__ == "Player":
            # Do not log
            result = RavenDB.QueryPlayer(object.PLAYER_ID)
            if result != 0:
                return result
            else:
                return 0
        elif object.__class__.__name__ == "Team":
            result = RavenDB.QueryTeam(object.team_id)
            if result != 0:
                return result
            else:
                return 0


#if __name__ == '__main__':
    #file1 = open("Logs/Log.txt", "r")
    #Routing("CREATE", RavenDB.User(name="Hello" ,username="HelloUser", password="HelloPass", birthday='2022-10-2'))
    #result = Routing("READ", RavenDB.User(username="HelloUser", password="HelloPass"), "Login")
    #print(result)
    #print(neo4j.GetUser("HelloUser"))
    #print(Redis.LoginCheck("HelloUser", "HelloPass"))
    #print(neo4j.Login_Check("HelloUser", "HelloPass"))