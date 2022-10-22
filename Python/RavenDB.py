from pyravendb.store import document_store
import bcrypt
import time
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
    def __init__(self):
        self.playerid


class User(object):
    def __init__(self, username, hashPassword, balance=0, betID=[]):
        self.username = username
        self.hashPassword = hashPassword
        self.balance = balance
        self.betID = betID


def GetAllTeamInfo():
    nba_teams = teams.get_teams()
    teamList = []
    with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
        store.initialize()
        for team in nba_teams:
            temp = Team(team['id'], team['full_name'], team['abbreviation'], team['city'], team['state'],
                        team['year_founded'], team_members = [])
            teamfinder = commonteamroster.CommonTeamRoster(season='2021-22',
                                                           team_id=f'{team["id"]}',
                                                           league_id_nullable='00').get_dict()
            for x in teamfinder['resultSets'][0]['rowSet']:
                id = x[14]
                print(x)
                temp.team_members.append(id)
                print(f"{temp.team_id}|{temp.team_members}")
                with store.open_session() as session:
                    temp2 = list(session.query(object_type=Player).where_equals("PLAYER_ID", id))
                    if temp2 == []:
                        player = CreatePlayer(id)
                        if player is None:
                            break
                        session.store(CreatePlayer(id))
                        session.save_changes()
                        store.close()
                        break
            with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
                store.initialize()
                with store.open_session() as session:

                    session.store(temp)
                    session.save_changes()


def GetAllPlayerStats():
    nba_players = players.get_active_players()
    PlayerList = []
    for player in nba_players:
        PlayerList.append(GetPlayerStats(player['id']))
    return PlayerList


def GetPlayerStats(playerID):
    career = playercareerstats.PlayerCareerStats(player_id=f'{playerID}').get_dict()
    # might need validation if json is different format.
    if career['resultSets'][0]['rowSet'] != []:
        i = len(career['resultSets'][0]['rowSet'])
        row = career['resultSets'][0]['rowSet'][i - 1]
        tempPlayer = Player(row[0], row[1], row[2], row[3], row[4], row[5],
                            row[6], row[7], row[8], row[9], row[10], row[11],
                            row[12], row[13], row[14], row[15], row[16], row[17],
                            row[18], row[19], row[20], row[21],
                            row[22], row[23], row[24],
                            row[25], row[26])
        return tempPlayer


def CreateUser(username, password):
    # User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password, passwordSalt)
    temp = User(username, password)
    with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(temp)
            session.save_changes()


def StoreObject(object):
    with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            query_result = list(session.query(object_type=Player).where_equals("PLAYER_ID", object.PLAYER_ID))
            if query_result == []:
                session.store(object)
                session.save_changes()


def CreatePlayer(id):
    time.sleep(0.7)
    player = players.find_player_by_id(id)
    if player is not None:
        print(players.find_player_by_id(id))
        temp = GetPlayerStats(id)
        if temp is None:
            return
        temp.full_name = player['full_name']
        temp.first_name = player['first_name']
        temp.last_name = player['last_name']
        return temp


def StoreAllPlayers():
    nba_players = players.get_active_players()
    for player in nba_players:
        if player['id'] is not None:
            time.sleep(0.7)
            temp = GetPlayerStats(player['id'])
            if temp is not None:
                temp.full_name = player['full_name']
                temp.first_name = player['first_name']
                temp.last_name = player['last_name']
                # try:
                StoreObject(temp)
                # except:
                # print("ID already exists")


if __name__ == '__main__':
    # teamfinder = commonteamroster.CommonTeamRoster(season='2021-22',
    #                                                team_id=f'1610612738',
    #                                                league_id_nullable='00')
    # print(teamfinder.get_dict()['resultSets'][0]['rowSet'][0][14])
    GetAllTeamInfo()
    # StoreAllPlayers()
    #print(playercareerstats.PlayerCareerStats(player_id=1630552).get_dict())
    # with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
    #     store.initialize()
    #     print("hello 2")
    #     with store.open_session() as session:
    #         print("hello world")
    #         foo = User("PyRavenDB", "Password")
    #         session.store(foo)
    #         session.save_changes()
