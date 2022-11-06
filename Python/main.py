import pip
from datetime import datetime, timezone
import requests
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats
from nba_api.stats.static import teams
import json
import RavenDB
import numpy
import pandas
from nba_api.stats.endpoints import leaguegamefinder, boxscoreadvancedv2
from datetime import datetime
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
            league_id='00'
        )

        current_scoreboard_info.get_dict()
        f = open("demofile2.json", "a")
        f.write(json.dumps(current_scoreboard_info.get_dict()))
        f.close()

    except requests.exceptions.ConnectionError:
        print("Request failed.")
#ScratchPad
def GetWinningTeam(gameId):
    #gameid is a string
    gamefinder = leaguegamefinder.LeagueGameFinder(game_id_nullable=gameId).get_dict()['resultSets'][0]['rowSet']
    if gamefinder is not None:
        for games in gamefinder:
            #print(games)
            if games[4] == gameId:
                #print(games[1])
                return games[1]
    return None
    # games = gamefinder.get_data_frames()[0]
    # games_1718 = games[games.GAME_ID == str(gameId)]['WL']
    # #for item in games_1718:
    # print(games_1718)
    # print(gamefinder.get_dict()['resultSets'][0]['rowSet'][0])
def GetGame(date):
    current_scoreboard_info = scoreboardv2.ScoreboardV2(
        day_offset=0,
        game_date=date,
        league_id='00'
    )
    matchList = []
    dataset = current_scoreboard_info.get_dict()['resultSets'][0]['rowSet']
    for data in dataset:
        #GAME_ID = 2, HOME_TEAM_ID = 6, VISITOR_TEAM_ID = 7, GAME_DATE_EST = 0
        winningTeamId = GetWinningTeam(data[2])
        date_time_str = data[0][:10]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d').strftime("%Y-%m-%d")
        if winningTeamId is None:
            match = RavenDB.Match(date_time_obj, int(data[2]), int(data[6]), int(data[7]))
        else:
            match = RavenDB.Match(date_time_obj, int(data[2]), int(data[6]), int(data[7]), int(winningTeamId))
        matchList.append(match)
    # for match in matchList:
    #     RavenDB.CreateTeam(match)
    return matchList
        #print(json.dumps(match.__dict__))


    #print(games.head())
    #print(games.groupby(games.SEASON_ID.str[-4:])[['GAME_ID']].count().loc['2022':])
    #games_1718 = games[games.GAME_ID == '0012200018']
    #print(games_1718)

    #game = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id='0012200018')
    #games = game.get_data_frames()[0]
    #f = open("demofile2.json", "w")
    #print(games['resultSets']['GAME_ID'])
    #f.write(json.dumps(game))
    #f.close()

    #print(games.head())

if __name__ == '__main__':
    GetGame('2022-10-6')
    #GetWinningTeam('0012200018')
#     print("X")
    #GetPlayerStats(203076)

