import pip
from datetime import datetime, timezone

import requests
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats
from nba_api.stats.static import teams
import json
import numpy
import pandas
class Players(object):
    def __init__(self, PLAYER_ID, SEASON_ID,LEAGUE_ID,
                 TEAM_ID,TEAM_ABBREVIATION, PLAYER_AGE,GP,
                 GS,MIN,FGM,FGA,FG_PCT,FG3M,FG3A,FG3_PCT,
                 FTM,FTA,FT_PCT,OREB,DREB,REB,AST,STL,BLK,TOV,PTS):
        self.PLAYER_ID
        self.SEASON_ID
        self.LEAGUE_ID
        self.TEAM_ID
        self.TEAM_ABBREVIATION
        self.PLAYER_AGE
        self.GP;
        self.GS
        self.MIN
        self.FGM
        self.FGA
        self.FG_PCT
        self.FG3M
        self.FG3A
        self.FG3_PCT
        self.FTM
        self.FTA
        self.FT_PCT
        self.OREB
        self.DREB
        self.REB
        self.AST
        self.STL
        self.BLK
        self.TOV
        self.PF
        self.PTS
def GetPlayerStats(playerID):
    career = playercareerstats.PlayerCareerStats(player_id=f'{playerID}')
    #might need validation if json is different format.
    print(json.dumps(career.get_dict()['resultSets'][0]['rowSet']))
    f = open("playerdemo.json", "a")
    #f.write(json.dumps(career.get_dict()['resultSets'][0]))
    f.close()
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
    GetPlayerStats(203076)

