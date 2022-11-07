from pyravendb.store import document_store
import bcrypt
import time
import uuid
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats, \
    commonteamroster
from nba_api.stats.static import teams, players
import pip
from datetime import datetime, timezone
import requests
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats, \
    commonteamroster
from nba_api.stats.static import teams, players
import json
import numpy
import pandas


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
class Match(object):
    def __init__(self, date, matchID, homeTeamID, awayTeamID, winningTeamID = None):
        self.Id = f'Match/{matchID}'
        self.matchId = matchID
        self.date = date
        self.homeTeamId = homeTeamID
        self.awayTeamID = awayTeamID
        self.winningTeamID = winningTeamID
class Bet(object):
    def __init__(self, id, user, type, matchId, status):
        #Id = uuid.uuid1()
        self.Id = f'Match/{id}'
        self.betId = id
        self.user = user
        self.matchId = matchId
        self.type = type
        self.status = status

class User(object):
    def __init__(self, username, hashPassword = None,name = None, password = None, birthday = None, balance=0, betID=[], friends = []):
        self.username = username
        self.hashPassword = hashPassword
        self.birthday = birthday
        self.password = password
        self.name = name
        self.balance = balance
        self.betID = betID
        self.friends = friends
global IPList
IPList = ['http://137.112.104.162:8080', 'http://137.112.104.155:8080', 'http://137.112.104.152:8080']


def CreateMatch(match):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(match)
            session.save_changes()
def EditMatch(match):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            tempmatch = session.load(f"Match/{match.matchId}")
            tempmatch.winningTeamID = match.winningTeamID
            session.save_changes()
def StoreTeam(team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            if QueryTeam(team.team_id) == []:
                session.store(team)
                session.save_changes()

def QueryTeam(id):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("team_id", id))
            return query_result

def EditTeam(team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("team_id", team.team_id))
            if query_result == []:
                session.store(team)
                session.save_changes()

def QueryPlayer(playerId):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp2 = list(session.query().where_equals("PLAYER_ID", playerId))
            if temp2 != []:
                return temp2.pop()
            else:
                return None
def StorePlayer(object):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("PLAYER_ID", object.PLAYER_ID))
            if query_result == []:
                session.store(object)
                session.save_changes()
def CreateBet(bet):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("betId", bet.betId))
            if query_result == []:
                session.store(bet)
                session.save_changes()
def EditBet(bet):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            tempBet = session.load(f"Bet/{bet.betId}")
            tempBet.status = bet.status
            session.save_changes()
def GetBet(id):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("betId", id))
            return query_result

def QueryUser(username):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("username", username))
            return query_result
def CreateUser(name, username, password, birthday):
    # User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    password =  password.encode('utf-8')
    hashPassword = bcrypt.hashpw(password, passwordSalt)
    temp = User(name=name, username=username, hashPassword=hashPassword.decode('utf-8'), birthday=birthday)
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("username", username))
            if query_result == []:
                session.store(temp)
                session.save_changes()
                return 1
            else:
                return 0


def LoginCheck(username, password):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("username", username))
            if query_result != []:
                passwordHash = query_result[0].hashPassword
                if bcrypt.checkpw(password.encode("utf-8"), passwordHash.encode("utf-8")):
                    return True
                else:
                    return False
            else:
                return False
def TestConnection():
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            a = session.query()
            return a

def StoreObject(object):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("PLAYER_ID", object.PLAYER_ID))
            if query_result == []:
                session.store(object)
                session.save_changes()


#if __name__ == '__main__':
    # teamfinder = commonteamroster.CommonTeamRoster(season='2021-22',
    #                                                team_id=f'1610612738',
    #                                                league_id_nullable='00')
    # print(teamfinder.get_dict()['resultSets'][0]['rowSet'][0][14])
    # GetAllTeamInfo()
    # StoreAllPlayers()

    # with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
    #     store.initialize()
    #     with store.open_session() as session:
    #         temp = User("sds", "2321")
    #         query_result = list(session.query(object_type=User).where_equals("username", "Username"))
    #         foo = session.load("User/Username", object_type=User)
    #         print(foo.username)
    #         foo.username = "Editted Username2"
    #         session.save_changes()
    #         query_result = list(session.query(object_type=User).where_equals("username", "Editted Username2"))
    #         print(json.dumps(query_result[0].__dict__))
    #         #print(query_result[0].Id)


    #CreateUser("Username", "Password")
    # print(playercareerstats.PlayerCareerStats(player_id=1630552).get_dict())
    # with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
    #     store.initialize()
    #     print("hello 2")
    #     with store.open_session() as session:
    #         print("hello world")
    #         foo = User("PyRavenDB", "Password")
    #         session.store(foo)
    #         session.save_changes()