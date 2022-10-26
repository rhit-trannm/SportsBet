from Python import neo4j
from Python import RavenDB
from py2neo import Graph
from pyravendb.store import document_store
import json
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

def LogRedis():
    print('x')
def LogNeo4J():
    print('x')
def UpdateNeo4J():
    print('x')
def UpdateRedis():
    print('x')

if __name__ == '__main__':


    print('x')