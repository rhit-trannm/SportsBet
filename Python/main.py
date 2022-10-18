import pip
from datetime import datetime, timezone
import requests
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats, commonteamroster
from nba_api.stats.static import teams, players
import json
import numpy
import pandas
class Player(object):
    def __init__(self, PLAYER_ID, SEASON_ID,LEAGUE_ID,
                 TEAM_ID,TEAM_ABBREVIATION, PLAYER_AGE,GP,
                 GS,MIN,FGM,FGA,FG_PCT,FG3M,FG3A,FG3_PCT,
                 FTM,FTA,FT_PCT,OREB,DREB,REB,AST,STL,BLK,TOV,PF,PTS):
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
                 state, year_founded, team_members = []):
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
def GetAllTeamInfo():
    nba_teams = teams.get_teams()
    teamList = []
    for team in nba_teams:
        temp = Team(team[0], team[1], team[2], team[3], team[4], team[5], team[6])
        nba_players = players.get_players()
        for player in nba_players:
            temp2 = GetPlayerStats(player['id'])
            if temp2.TEAM_ID == temp.team_id:
                temp.team_members.append(temp2.PLAYER_ID)
    return teamList
def GetAllPlayerStats():
    nba_players = players.get_players()
    PlayerList = []
    for player in nba_players:
        PlayerList.append(GetPlayerStats(player['id']))
    return PlayerList
def GetPlayerStats(playerID):
    career = playercareerstats.PlayerCareerStats(player_id=f'{playerID}').get_dict()
    #might need validation if json is different format.
    if career['resultSets'][0]['rowSet'] != []:
        for row in career['resultSets'][0]['rowSet']:
            if(row[1] == '2021-22'):
                tempPlayer = Player(row[0],row[1], row[2], row[3], row[4], row[5],
                                    row[6], row[7], row[8], row[9], row[10], row[11],
                                    row[12], row[13], row[14], row[15], row[16], row[17],
                                    row[18],row[19], row[20], row[21],
                                    row[22], row[23], row[24],
                                    row[25], row[26])
                return tempPlayer
    #print(json.dumps(career.get_dict()['resultSets'][0]['rowSet']))
    #f = open("playerdemo.json", "a")
    #f.write(json.dumps(career.get_dict()['resultSets'][0]))
    #f.close()
def GetScoreboard():
    day_offset = 0
    date = "2022-10-5"
    id = '00'
    try:
        current_scoreboard_info = scoreboardv2.ScoreboardV2(
            day_offset=0,
            game_date=date,
            league_id=id
        )

        current_scoreboard_info.get_dict()
        f = open("demofile2.json", "a")
        f.write(json.dumps(current_scoreboard_info.get_dict()))
        f.close()

    except requests.exceptions.ConnectionError:
        print("Request failed.")
#ScratchPad
if __name__ == '__main__':
    nba_teams = players.get_players()
    print(nba_teams[0])
#     print("X")
    #GetPlayerStats(203076)

