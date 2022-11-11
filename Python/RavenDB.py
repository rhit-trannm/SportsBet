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
    def __init__(self, full_name, first_name, last_name, PLAYER_ID, SEASON_ID, LEAGUE_ID,
                 TEAM_ID, TEAM_ABBREVIATION, PLAYER_AGE, GP,
                 GS, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT,
                 FTM, FTA, FT_PCT, OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS):
        self.Id = f'Player/{PLAYER_ID}'
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name
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


class PlayerGame(object):
    def __init__(self, PLAYER_ID, GAME_ID, GAME_DATE, MATCHUP, WL, MIN, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT,
        OREB, DREB, REB, AST, STL, BLK, TOV, PF, PTS, PLUS_MINUS):
        self.PLAYER_ID = PLAYER_ID
        self.GAME_ID = GAME_ID
        self.GAME_DATE = GAME_DATE
        self.MATCHUP = MATCHUP
        self.WL = WL
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
        self.PLUS_MINUS = PLUS_MINUS

class TeamSeason(object):
    def __init__(self, TEAM_ID, TEAM_CITY, TEAM_NAME, YEAR, GP, WINS, LOSSES, WIN_PCT, CONF_RANK, DIV_RANK, PO_WINS, PO_LOSSES,
        FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, REB, AST, PF, STL, TOV, BLK, PTS, PTS_RANK):
        self.Id = f'{TEAM_ID}/{YEAR}'
        self.TEAM_ID = TEAM_ID
        self.TEAM_CITY = TEAM_CITY
        self.TEAM_NAME = TEAM_NAME
        self.YEAR = YEAR
        self.GP = GP
        self.WINS = WINS
        self.LOSSES = LOSSES
        self.WIN_PCT = WIN_PCT
        self.CONF_RANK = CONF_RANK
        self.DIV_RANK = DIV_RANK
        self.PO_WINS = PO_WINS
        self.PO_LOSSES = PO_LOSSES
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
        self.PTS_RANK = PTS_RANK
        
class Match(object):
    def __init__(self, date, matchId, homeTeamId, awayTeamID, winningTeamID = None):
        self.Id = f'Match/{matchId}'
        self.matchId = matchId
        self.date = date
        self.homeTeamId = homeTeamId
        self.awayTeamID = awayTeamID
        self.winningTeamID = winningTeamID


class overUnderBet(object):
    def __init__(self, amount, user, isUnder, matchId, status='PENDING'):
        #Id = uuid.uuid1()
        self.Id = f'BetOU/{user}/{matchId}'
        self.amount = amount
        self.user = user
        self.matchId = matchId
        self.isUnder = isUnder
        self.status = status

class moneyLineBet(object):
    def __init__(self, winner, amount, user, matchId, status='PENDING'):
        self.Id = f'BetML/{user}/{matchId}'
        self.winner = winner
        self.amount = amount
        self.user = user
        self.matchId = matchId
        self.status = status

class User(object):
    def __init__(self, username, hashPassword = None,name = None, password = None, birthday = None, balance=0, betID=[], friends = []):
        self.Id = f'User/{username}'
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

def GetMatches(date):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            games = list(session.query(object_type=Match).where_equals("date", date))
            if len(games)==0:
                return None
            else:
                return games


def StoreTeam(team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            if QueryTeam(team.team_id) is None:
                session.store(team)
                session.save_changes()
    

def QueryTeam(id):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=Team).where_equals("team_id", id))
            if len(query_result) == 0:
                return None
            return query_result.pop()


def EditTeam(team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query().where_equals("team_id", team.team_id))
            if query_result == []:
                session.store(team)
                session.save_changes()
            else:
                session.delete(f"Team/{team.team_id}")
                session.store(team)
                session.save_changes()

    
def EditPlayer(player):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            if QueryPlayer(player.PLAYER_ID) is not None:
                tempBet = session.delete(f"Player/{player.PLAYER_ID}")
                session.store(player)
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

def SearchPlayerName(name):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp = list(session.query(object_type=Player).where_equals("full_name", name))
            temp1 = list(session.query(object_type=Player).where_equals("first_name", name))
            temp2 = list(session.query(object_type=Player).where_equals("last_name", name))
            results = temp+temp1+temp2
            if len(results)>0:
                return results
            else:
                return None


def SearchPlayerTeam(team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp = list(session.query(object_type=Player).where_equals("TEAM_ABBREVIATION", team))
            if len(temp)>0:
                return temp
            else:
                return None

def SearchPlayerNameTeam(name, team):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp = list(session.query(object_type=Player).where_equals("full_name", name).and_also().where_equals("TEAM_ABBREVIATION", team))
            temp1 = list(session.query(object_type=Player).where_equals("first_name", name).and_also().where_equals("TEAM_ABBREVIATION", team))
            temp2 = list(session.query(object_type=Player).where_equals('last_name',name).and_also().where_equals('TEAM_ABBREVIATION',team))
            temp3 = temp+temp1+temp2
            if len(temp3)>0:
                return temp3
            else:
                return None

def SearchPlayers():
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp = list(session.query(object_type=Player))
            if len(temp)>0:
                return temp
            else:
                return None

def StoreGame(object):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=PlayerGame).where_equals("PLAYER_ID", object.PLAYER_ID).and_also().where_equals("GAME_ID", object.GAME_ID))
            if query_result == []:
                session.store(object)
                session.save_changes()


def StoreSeason(object):
    with document_store.DocumentStore(urls=IPList[0], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=TeamSeason).where_equals("TEAM_ID", object.TEAM_ID).and_also().where_equals("YEAR", object.YEAR))
            if len(query_result)>0:
                session.delete(f'{object.TEAM_ID}/{object.YEAR}')
            session.store(object)
            session.save_changes()

def GetSeason(teamID):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=TeamSeason).where_equals("TEAM_ID", teamID))
            return query_result.pop()



def QueryPlayerGames(playerId):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            temp2 = list(session.query(object_type=PlayerGame).where_equals("PLAYER_ID", playerId))
            if len(temp2) > 0:
                return temp2
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
            query_result = list(session.query(object_type=User).where_equals("username", username))
            return query_result

def getUsers():
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=User))
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

def deleteUser(userID):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.delete(f"User/{userID}")
            return




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
def DeleteDocument(obj):
    with document_store.DocumentStore(urls=[IPList[0]], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.delete(obj.Id)
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