from Python import neo4j
from Python import RavenDB
from Python import Redis
from py2neo import Graph
from pyravendb.store import document_store
from types import SimpleNamespace
import json
import os
import pymongo
from pymongo import MongoClient
from pymongo import ReturnDocument


client = MongoClient('mongodb://logUser:abcd123@433-16.csse.rose-hulman.edu/?authMechanism=DEFAULT') 

db = client['logs']

counters = db['counter']

def get_id(db):
    new_id = counters.find_one_and_update({'_id':db}, {'$inc':{'last_written':1}}, return_document=ReturnDocument.AFTER)
    return new_id['last_written']

'_id':get_id('raven')



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

class Player(object):
    def __init__(self, PLAYER_ID, SEASON_ID, LEAGUE_ID,
                 TEAM_ID, TEAM_ABBREVIATION, PLAYER_AGE, GP,
                 GS, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
                 FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS):
        self.Id = f'Player/{PLAYER_ID}'
        self.full_name = None
        self.first_name = None
        self.last_name = None
        self.PLAYER_ID = PLAYER_ID
        self.SEASON_ID = SEASON_ID
        self.LEAGUE_ID = LEAGUE_ID
        self.TEAM_ID = TEAM_ID
        self.TEAM_ABBREVIATION = TEAM_ABBREVIATION
        self.PLAYER_AGE = PLAYER_AGE
        self.GP = GP
        self.GS = GS
        self.MIN = MIN
        self.FGM = FGM
        self.FGA = FGA
        self.FG_PCT = FG_PCT
        self.FG3M = FG3M
        self.FG3A = FG3A
        self.FG3_PCT = FG3_PCT
        self.FTM = FTM
        self.FTA = FTA
        self.FT_PCT = FT_PCT
        self.OREB = OREB
        self.DREB = DREB
        self.REB = REB
        self.AST = AST
        self.STL = STL
        self.BLK = BLK
        self.TOV = TOV
        self.PF = PF
        self.PTS = PTS


class Team(object):
    def __init__(self, team_id, full_name, abbreviation, city,
                 state, year_founded, team_members=[]):
        self.Id = f'Team/{team_id}'
        self.team_id = team_id
        self.full_name = full_name
        self.abbreviation = abbreviation
        self.city = city
        self.state = state
        self.year_founded = year_founded
        self.team_members = team_members


class User(object):
    def __init__(self, username, hashPassword, balance=0, betID=[]):
        self.username = username
        self.hashPassword = hashPassword
        self.balance = balance
        self.betID = betID


class LogObject(object):
    def __init__(self, command, classObject, className):
        self.command = command
        self.classObject = classObject
        self.className = className


def Logging(CRUD, classObject):
    # Need Individual Files for different database to keep track of up to dateness
    redisLog = open("Logs/RedisLog.txt", "r")
    neo4JLog = open("Logs/Neo4JLog.txt", "r")
    # Load into python list
    check_file = os.stat("Logs/RedisLog.txt").st_size
    check_file2 = os.stat("Logs/Neo4JLog.txt").st_size
    redisEventList = []
    neo4JEventList = []
    if (check_file != 0):
        redisEventList = json.loads(redisLog.read())
    else:
        redisEventList = []
    if (check_file2 != 0):
        neo4JEventList = json.loads(neo4JLog.read())
    else:
        neo4JEventList = []

    redisLog.close()
    neo4JLog.close()
    # This isn't safe but no other solution for now
    redisLog = open("Logs/RedisLog.txt", "w")
    neo4JLog = open("Logs/Neo4JLog.txt", "w")
    print(redisEventList)
    # Create log entry
    logEntry = LogObject(CRUD, classObject.__dict__, classObject.__class__.__name__).__dict__
    # Add to list of event
    if(CRUD == 'CREATE' & object.__class__.__name__ == "User"): #go to all 3 databases
        logEntry['_id'] = get_id('redis')
        db.redis.insert_one(logEntry)
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'CREATE' & object.__class__.__name__ == "Bet"):
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
    if(CRUD == 'UPDATE' & object.__class__.__name__ == "User"):
        logEntry['_id'] = get_id('redis')
        db.redis.insert_one(logEntry)
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'UPDATE' & object.__class__.__name__ == "Bet"):
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
    if(CRUD == 'UPDATE' & object.__class__.__name__ == "Player"):
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'UPDATE' & object.__class__.__name__ == "Team"):
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'DELETE' & object.__class__.__name__ == "User"):
        logEntry['_id'] = get_id('redis')
        db.redis.insert_one(logEntry)
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'DELETE' & object.__class__.__name__ == "Bet"):
        logEntry['_id'] = get_id('neo')
        db.neo.insert_one(logEntry)
    if(CRUD == 'DELETE' & object.__class__.__name__ == "Player"):
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)
    if(CRUD == 'DELETE' & object.__class__.__name__ == "Team"):
        logEntry['_id'] = get_id('raven')
        db.raven.insert_one(logEntry)

    #NEED TO ADD FRIEND COMMANDS HERE EVENTUALLY
    
    redisEventList.append(logEntry)
    neo4JEventList.append(logEntry)
    # Write to file

    redisLog.truncate()
    neo4JLog.truncate()

    redisLog.write(json.dumps(redisEventList))
    neo4JLog.write(json.dumps(neo4JEventList))

    redisLog.close()
    neo4JLog.close()


def Routing(CRUD, object, command):
    # Theory: CUD should all go through RavenDB first. RavenDB acts as a Master database.
    # Any changes should go through RavenDB first. Read should be routed to its approriate database.
    if CRUD == "CREATE":
        try:
            if object.__class__.__name__ == "User":
                try:
                    RavenDB.CreateUser(object.username, object.hashPassword)
                    Logging(CRUD, object)
                    return 1
                except:
                    return 0
            elif object.__class__.__name__ == "Bet":
                print('x')
        except:
            return 0
    elif CRUD == "READ": #Not stored in Mongo, rather is sent directly to databases
        #Need to check if each database is up to date according to logs.
        if object.__class__.__name__ == "User":
            if command == "Login":
                try:
                    if RavenDB.LoginCheck(object.username, object.hashPassword) == True:
                        return True
                    else:
                        return False
                except:
                    try:
                        if neo4j.Login_Check(object.username, object.hashPassword) == True:
                            return True
                        else:
                            return False
                    except:
                        if Redis.LoginCheck(object.username, object.hashPassword) == True:
                            return True
                        else:
                            return False
            elif command == "GetUser":
                try:
                    if Redis.GetUser(object.username) == True:
                        return True
                    else:
                        return False
                except:
                    try:
                        if neo4j.GetUser(object.username) == True:
                            return True
                        else:
                            return False
                    except:
                        if RavenDB.LoginCheck(object.username, object.hashPassword) == True:
                            return True
                        else:
                            return False

        elif object.__class__.__name__ == "Bet":
            print('x')
        elif object.__class__.__name__ == "Player":
            # Do not log
            result = RavenDB.QueryPlayer(object.PLAYER_ID)
            if result != 0:
                return result
            else:
                return 0
        elif object.__class__.__name__ == "Team":
            # Do not log
            print('x')
    elif CRUD == "UPDATE":
        try:
            if object.__class__.__name__ == "User":
                RavenDB.CreateUser(object.username, object.hashPassword)
                Logging(CRUD, object)
                return 1
            elif object.__class__.__name__ == "Bet":
                print('x')
            elif object.__class__.__name__ == "Player":
                # Do not log
                print('x')
            elif object.__class__.__name__ == "Team":
                # Do not log
                print('x')
        except:
            return 0
        print("x")
    elif CRUD == "DELETE":
        try:
            if object.__class__.__name__ == "User":
                RavenDB.CreateUser(object.username, object.hashPassword)
                Logging(CRUD, object)
                return 1
            elif object.__class__.__name__ == "Bet":
                print('x')
            elif object.__class__.__name__ == "Player":
                # Do not log
                print('x')
            elif object.__class__.__name__ == "Team":
                # Do not log
                print('x')
        except:
            return 0


# CRUD for each object. if success then log.


def UpdateNeo4J():
    #these updates should be multithreaded.
    neo4JLog = open("Logs/Neo4JLog.txt", "r")


def UpdateRedis():
    redisLog = open("Logs/RedisLog.txt", "r")
    temp2 = json.loads(redisLog.read(), object_hook=lambda d: SimpleNamespace(**d))
    for item in temp2:
        print(json.loads(item))


if __name__ == '__main__':
    # file1 = open("Logs/Log.txt", "r")
    print(Routing("CREATE", User('johnd', 'password123'), "Login"))
    ########## Loading & Adding JSON List example ##############

    # file1 = open("Logs/Log.txt", "r")
    # temp2 = json.loads(file1.read(), object_hook=lambda d: SimpleNamespace(**d))
    # temp2.append(json.dumps(LogObject("ADD", json.dumps(User("user", "pass").__dict__), "User").__dict__))
    # print(f"{temp2}")

    ########## Loading & Adding JSON List example ##############

    ########## Storing List as JSON example ##############

    # file1 = open("Logs/Log.txt", "a")
    # temp = LogObject("ADD", json.dumps(User("user", "pass").__dict__), "User")
    # temp2 = LogObject("ADD", json.dumps(User("user2", "pass2").__dict__), "User")
    # lists = [json.dumps(temp.__dict__), json.dumps(temp2.__dict__)]
    # file1.write(json.dumps(lists))

    ########## Storing List as JSON example ##############