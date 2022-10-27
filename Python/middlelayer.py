from Python import neo4j
from Python import RavenDB
from Python import Redis
from py2neo import Graph
from pyravendb.store import document_store
from types import SimpleNamespace
import json
import os
#Principles When coding middle layer:
#Read does not need to get written to file
#Write needs to get written to file

#routing logic: Ping each database before performing action. Check if they are up.
#Check if up to date,
#If it is not -> reroute and update it while rerouting.
#If it is -> Use database.

#User -> Duplicated on all 3 database. Should follow this roadmap... Redis -> Neo4j -> RavendB
#Bets -> Duplicated on Neo4J and RavenDB. Neo4J -> RavenDB.
#NBA Teams/Player info -> On RavenDB. Should never go down.

#In general, RavenDB should never go down. If it does go down, the entire system should go down.

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
    def __init__(self, command, classObject, classType):
        self.command = command
        self.classObject = classObject
        self.classType = classType
def Logging(CRUD, classObject):
    #Need Individual Files for different database to keep track of up to dateness
    redisLog = open("Logs/RedisLog.txt", "r")
    neo4JLog = open("Logs/Neo4JLog.txt", "r")
    #Load into python list
    check_file = os.stat("Logs/RedisLog.txt").st_size
    check_file2 = os.stat("Logs/Neo4JLog.txt").st_size
    if(check_file == 0):
        redisEventList = json.loads(redisLog.read())
    else:
        redisEventList = []
    if(check_file2 == 0):
        neo4JEventList = json.loads(neo4JLog.read())
    else:
        neo4JEventList = []

    redisLog.close()
    neo4JLog.close()
    #This isn't safe but no other solution for now
    redisLog = open("Logs/RedisLog.txt", "w")
    neo4JLog = open("Logs/Neo4JLog.txt", "w")
    print(redisEventList)
    #Create log entry
    logEntry = json.dumps(LogObject(CRUD, json.dumps(classObject.__dict__), classObject.__class__.__name__).__dict__)
    #Add to list of event
    redisEventList.append(logEntry)
    neo4JEventList.append(logEntry)
    #Write to file

    redisLog.truncate()
    neo4JLog.truncate()

    redisLog.write(json.dumps(redisEventList))
    neo4JLog.write(json.dumps(neo4JEventList))

    redisLog.close()
    neo4JLog.close()

def Routing(CRUD, object):
    #Theory: CUD should all go through RavenDB first. RavenDB acts as a Master database.
    #Any changes should go through RavenDB first. Read should be routed to its approriate database.
    if CRUD == "CREATE":
        print("x")
    elif CRUD == "READ":
        print("x")
    elif CRUD == "UPDATE":
        print("x")
    elif CRUD == "DELETE":
        print("x")

    #CRUD for each object. if success then log.




def UpdateNeo4J():
    neo4JLog = open("Logs/Neo4JLog.txt", "r")
def UpdateRedis():
    redisLog = open("Logs/RedisLog.txt", "r")
    temp2 = json.loads(redisLog.read(), object_hook=lambda d: SimpleNamespace(**d))
    for item in temp2:
        print(json.loads(item))


if __name__ == '__main__':
    #file1 = open("Logs/Log.txt", "r")
    UpdateRedis()
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