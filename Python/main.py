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

#ScratchPad
class FooBar(object):
    def __init__(self, name, foo):
        self.name = name
        self.foo = foo
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
def GetPlayerStats():
    career = playercareerstats.PlayerCareerStats(player_id='203076')
    f = open("playerdemo.json", "a")
    f.write(json.dumps(career.get_dict()))
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

if __name__ == '__main__':
    GetPlayerStats()



