import time
import middlelayer
import numpy as np
import pip
from datetime import datetime, timezone
import requests
from dateutil import parser
from nba_api.live.nba.endpoints import scoreboard
from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats, \
    commonteamroster, playergamelog, teamyearbyyearstats
from nba_api.stats.static import teams, __all__, players
import json
import RavenDB
import numpy
import pandas
from nba_api.stats.endpoints import leaguegamefinder, boxscoreadvancedv2
from datetime import datetime


def GetPlayerStats(playerID):
    career = playercareerstats.PlayerCareerStats(player_id=f'{playerID}').get_dict()
    # might need validation if json is different format.
    if career['resultSets'][0]['rowSet'] != []:
        for row in career['resultSets'][0]['rowSet']:
            if (row[1] == '2022-23'):
                tempPlayer = RavenDB.Player(row[0], row[1], row[2], row[3], row[4], row[5],
                                            row[6], row[7], row[8], row[9], row[10], row[11],
                                            row[12], row[13], row[14], row[15], row[16], row[17],
                                            row[18], row[19], row[20], row[21],
                                            row[22], row[23], row[24],
                                            row[25], (row[26]/row[10]))
                return tempPlayer
    # print(json.dumps(career.get_dict()['resultSets'][0]['rowSet']))
    # f = open("playerdemo.json", "a")
    # f.write(json.dumps(career.get_dict()['resultSets'][0]))
    # f.close()

def GetPlayerGames(playerID):
    games = playergamelog.PlayerGameLog(player_id=str(playerID)).get_dict()
    # might need validation if json is different format.
    if len(games['resultSets'][0]['rowSet']) > 0:
        tempPlayerGames = [RavenDB.PlayerGame(row[1], row[2], row[3], row[4], row[5],
                                    row[6], row[7], row[8], row[9], row[10], row[11],
                                    row[12], row[13], row[14], row[15], row[16], row[17],
                                    row[18], row[19], row[20], row[21],
                                    row[22], row[23], row[24], row[25]) for row in games['resultSets'][0]['rowSet']]
        return tempPlayerGames


def GetAllTeamInfo():
    nba_teams = teams.get_teams()
    teamList = []
    for team in nba_teams:
        temp = RavenDB.Team(team['id'], team['full_name'], team['abbreviation'], team['city'], team['state'],
                            team['year_founded'], team_members=[])
        teamfinder = commonteamroster.CommonTeamRoster(team_id=f'{team["id"]}', league_id_nullable='00').get_dict()
        for x in teamfinder['resultSets'][0]['rowSet']:
            id = x[14]
            temp.team_members.append(id)
        middlelayer.Routing("CREATE", temp)


def GetTeamSeason(teamID):
    season = teamyearbyyearstats.TeamYearByYearStats(team_id=str(teamID)).get_dict()
    if len(season['resultSets'][0]['rowSet'])>0:
        row = season['resultSets'][0]['rowSet'][-1]
        temp = RavenDB.TeamSeason(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                        row[10], row[11], np.round(row[15]/row[4],2), np.round(row[16]/row[4],2), row[17],
                        np.round(row[18]/row[4],2), np.round(row[19]/row[4],2), row[20], np.round(row[21]/row[4],2),
                        np.round(row[22]/row[4],2), row[23], np.round(row[24]/row[4],2), np.round(row[25]/row[4],2),
                        np.round(row[26]/row[4],2), np.round(row[27]/row[4],2), np.round(row[28]/row[4],2),
                        np.round(row[29]/row[4],2), np.round(row[30]/row[4],2), np.round(row[31]/row[4],2),
                        np.round(row[32]/row[4],2), row[33])
        return temp


def StoreAllTeamSeasons():
    nba_teams = teams.get_teams()
    for team in nba_teams:
        if team['id'] is not None:
            time.sleep(0.7)
            temp = GetTeamSeason(team['id'])
            if temp is not None:
                middlelayer.Routing("CREATE", temp)

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
                middlelayer.Routing("CREATE", temp)
                # StoreObject(temp)
                # except:
                # print("ID already exists")


def StoreAllPlayerGames():
    nba_players = players.get_active_players()
    for player in nba_players:
        if player['id'] is not None:
            time.sleep(0.7)
            temp = GetPlayerGames(player['id'])
            if temp is not None:
                for game in temp:
                    middlelayer.Routing("CREATE", game)



def GetScoreboard(date):
    day_offset = 0
    date = date
    id = '00'
    try:
        current_scoreboard_info = scoreboardv2.ScoreboardV2(
            day_offset=0,
            game_date=date,
            league_id='00'
        )

        games = current_scoreboard_info.get_dict()['resultSets'][0]['rowSet'][0]
        for g in games:
            temp = RavenDB.Match(g[0][:-9], g[4], g[2], g[6], g[7])
            middlelayer.Routing("CREATE", temp)

    except requests.exceptions.ConnectionError:
        print("Request failed.")


# ScratchPad
def GetWinningTeam(gameId):
    # gameid is a string
    gamefinder = leaguegamefinder.LeagueGameFinder(game_id_nullable=gameId).get_dict()['resultSets'][0]['rowSet']
    if gamefinder is not None:
        for games in gamefinder:
            # print(games)
            if games[4] == gameId:
                # print(games[1])
                return games[1]
    return None
    # games = gamefinder.get_data_frames()[0]
    # games_1718 = games[games.GAME_ID == str(gameId)]['WL']
    # #for item in games_1718:
    # print(games_1718)
    # print(gamefinder.get_dict()['resultSets'][0]['rowSet'][0])


def GetGame(date):
    #Format 2022-10-6
    current_scoreboard_info = scoreboardv2.ScoreboardV2(
        day_offset=0,
        game_date=date,
        league_id='00'
    )
    matchList = []
    dataset = current_scoreboard_info.get_dict()['resultSets'][0]['rowSet']
    for data in dataset:
        # GAME_ID = 2, HOME_TEAM_ID = 6, VISITOR_TEAM_ID = 7, GAME_DATE_EST = 0
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
    for match in matchList:
        middlelayer.Routing("CREATE", match)
    return matchList


def CheckWinning(match):
    result = GetWinningTeam(match.matchId)
    if result is not None:
        match.winningTeamID = result
    else:
        return None
def AutomaticPinging():
    StoreAllPlayers()
    GetAllTeamInfo()
    time.sleep(86400)
def Test():
    StoreAllTeamSeasons()


    # print(games.head())
if __name__ == '__main__':
    Test()
    while(True):
        AutomaticPinging()
#     GetGame('2022-10-6')
    # GetWinningTeam('0012200018')
#     print("X")
# GetPlayerStats(203076)
