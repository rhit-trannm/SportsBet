from py2neo import Graph
import bcrypt
from pyravendb.store import document_store



def ConnectNeo4J():
    global graph
    graph = Graph("bolt://433-15.csse.rose-hulman.edu:7687", auth=("neo4j", "433-15")) #EDIT THIS TO BE ACCURATE -Josh Mestemacher

def CheckConnection():
    try:
        graph.run("Match () return 1 limit 1")
    except Exception:
        print('Connection Error')


def Get_Number_Of_Friends(username):
    cursor  = graph.run(f"MATCH (User1)-[r:friend_of]-(User2)\nWHERE User1.username = '{username}' \nRETURN COUNT(r)")
    friendCount = cursor.evaluate()
    return friendCount

def Get_Balance(username):
    cursor = graph.run(f"MATCH (User)\nWHERE User.username = '{username}' \nRETURN User.balance")
    balance = cursor.evaluate()
    return balance


def Create_User(name, username, password, birthday):
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    graph.run(f"CREATE (n:Person {{username: '{username}', passwordHash: '{hashPassword.decode()}', balance: {0}, fullName: '{name}', birthday: '{birthday}'}})")

def Login_Check(username, password):
   userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
   if(userExists):
    cursor = graph.run(f"MATCH(User) WHERE User.username = '{username}' RETURN User.passwordHash")
    passwordHash = cursor.evaluate()
    if bcrypt.checkpw(password.encode("utf-8"), passwordHash.encode("utf-8")):
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


