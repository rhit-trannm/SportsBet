from matplotlib.backend_bases import GraphicsContextBase
from py2neo import Graph
import bcrypt
from regex import F
from pyravendb.store import document_store



def ConnectNeo4J():
    global graph
    graph = Graph("bolt://433-16.csse.rose-hulman.edu:7687", auth=("neo4j", "123")) #EDIT THIS TO BE ACCURATE -Josh Mestemacher
    graph = Graph("localhost", auth=("neo4j", "123"))



def Get_Number_Of_Friends(username):
    ConnectNeo4J
    friendCount  = graph.run(f"MATCH (User1)-[r:friend_of]->(User2)\nWHERE User1.username =" + str(username) + "\nRETURN COUNT(r)")
    return friendCount

def Get_Balance(username):
    ConnectNeo4J
    balance = graph.run(f"MATCH (User)\nWHERE User.username =" + str(username) + "\nRETURN User.balance")
    return balance


def Create_User(username, password):
    ConnectNeo4J
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password, passwordSalt)
    graph.run(f"CREATE (n:Person {{username: '{username}', passwordHash: '{hashPassword}', balance: {0}}})")

def Login_Check(username, password):
   userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
   if(userExists):
    correctPassword = graph.run(f"MATCH(User) WHERE User.username = {username} RETURN User.passwordHash")
    if(password == correctPassword):
        return True

def Create_MoneyLine_Bet(game_date, winner_team_abbrev, amount_betted, username): #I assume team abbrev is a drop down for this,  and so is game
    ConnectNeo4J
    userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:MoneyLineBet {{user: '{username}', amountBetted: '{amount_betted}', winnerAbbrev: '{winner_team_abbrev}', game_date'{game_date}'}})")
            graph.run(f"MATCH (u:User) WHERE u.username = {username} SET u.balance = u.balance - {amount_betted}") #adjust user balance,

def Create_OverUnder_Bet(game_date, stat_type_abbrev, amount_betted, username, isUnder, stat_bet): #isUnder is 1 or 0 (meaning its an over bet), I assume isUnder will be a drop down
    #box, same for stat_type_abbrev, I assume amount_betted will be an integer. stat_bet is amount you are betting a stat will be under or over, technically in real betting not controlled by you
    userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:OverUnderBet {{user: '{username}', amountBetted: '{amount_betted}', isUnder: '{isUnder}', game_date: '{game_date}', stat_type: '{stat_type_abbrev}', stat_bet: '{stat_bet}'}})")
            graph.run(f"MATCH (u:User) WHERE u.username = {username} SET u.balance = u.balance - {amount_betted}") #adjust user balance,


