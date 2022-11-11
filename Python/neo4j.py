import json

from py2neo import Graph
import bcrypt
try:
    from Python import RavenDB
except:
    import RavenDB
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

def Check_Friend(user, friend):
    cursor  = graph.run(f"MATCH (User1)-[r:friend_of]-(User2)\nWHERE User1.username = '{user}' AND User2.username='{friend}' \nRETURN COUNT(r)")
    friendCount = cursor.evaluate()
    return friendCount

def Get_Balance(username):
    cursor = graph.run(f"MATCH (User)\nWHERE User.username = '{username}' \nRETURN User.balance")
    balance = cursor.evaluate()
    return balance

def add_balance(user, amount):
    graph.run(f"MATCH (u:User) WHERE u.username='{user}' SET u.balance=u.balance+{amount}")
    
def remove_balance(user, amount):
    cursor = graph.run(f"MATCH (u:User) WHERE u.username='{user}' SET u.balance=u.balance-{amount} RETURN u.balance")
    new_bal = cursor.evaluate()
    if new_bal < 0:
        add_balance(user, amount)

def Find_User(user):
    cursor = graph.run(f"MATCH (u:User) WHERE u.username='{user}' \nRETURN COUNT(u)")
    num = cursor.evaluate()
    return num
    
def GetUser(username):
    ConnectNeo4J()
    dataset = graph.run(f"MATCH (n:User {{username : '{username}'}}) RETURN n").data()
    if dataset != []:
        #print(json.loads(json.dumps(dataset.pop()['n'])))
        data = dataset.pop()['n']
        return RavenDB.User(username=data['username'], name=data['fullName'], hashPassword=data['passwordHash'], friends=data['friends'], birthday=data['birthday'])
        #return dataset.pop()['n']

def Create_User(name, username, password, birthday):
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    graph.run(f"CREATE (n:User {{username: '{username}', passwordHash: '{hashPassword.decode()}', balance: {0}, fullName: '{name}', birthday: '{birthday}', friends: []}})")
    #graph.run(f"CREATE CONSTRAINT usernameUniqueness ON (u:User) ASSERT u.username IS UNIQUE") #add constraint enforcing uniqueness of usernames


def Login_Check(username, password):
   userExists = graph.run(f"MATCH (u:User) WHERE u.username = '{username}' WITH COUNT(u) > {0} as node_exists RETURN node_exists")
   if(userExists):
    cursor = graph.run(f"MATCH(User) WHERE User.username = '{username}' RETURN User.passwordHash")
    passwordHash = cursor.evaluate()
    if bcrypt.checkpw(password.encode("utf-8"), passwordHash.encode("utf-8")):
        return True
    else:
        print("InnerShellFalse")
        return False

def Create_MoneyLine_Bet(winner_team_abbrev, amount_betted, username, gameId): #I assume team abbrev is a drop down for this,  and so is gameId and game_date
    ConnectNeo4J
    userExists = graph.run(f"MATCH (u:User) WHERE u.username = '{username}' WITH COUNT(u) > 0 as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:MoneyLineBet {{amount: {amount_betted}, winner: '{winner_team_abbrev}', gameID: '{gameId}', user: '{username}', Status: '{'Pending'}'}})")
            graph.run(f"MATCH (u:User {{username:'{username}'}}), (b:MoneyLineBet {{gameID: '{gameId}'}}) CREATE (u)-[r:BETS]->(b)")
            graph.run(f"MATCH (u:User) WHERE u.username = '{username}' SET u.balance = u.balance - {amount_betted}") #adjust user balance,

def Create_OverUnder_Bet_Player(stat_type_abbrev, amount_betted, username, isUnder, stat_bet, gameId, playerId): #isUnder is 1 or 0 (meaning its an over bet), I assume isUnder will be a drop down
    #box, same for stat_type_abbrev, I assume amount_betted will be an integer. stat_bet is amount you are betting a stat will be under or over, technically in real betting not controlled by you
    #I assume gameId and game_date and playerId is point and click or drop done or automatically determined by ravenDb and sent here as inputs.
    userExists = graph.run(f"MATCH (u:User) WHERE User.username = '{username}' WITH COUNT(u) > 0 as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:OverUnderBetPlayer {{user: '{username}', amountBetted: '{amount_betted}', playerId: '{playerId}', isUnder: '{isUnder}', stat_type: '{stat_type_abbrev}', stat_bet: '{stat_bet}', gameID: '{gameId}'}})")
            graph.run(f"MATCH (u:User) WHERE u.username = '{username}' SET u.balance = u.balance - {amount_betted}") #adjust user balance,


def Payout_MoneyLine_Bets(winningTeamID, gameId): #we assume a team can't play 2 games in one day for this method, going with double payout for now for simplicity's sake - Josh Mestemacher
    graph.run(f"MATCH (b:MoneyLineBet) WHERE b.gameID = {gameId} AND b.winner = {winningTeamID} AND b.Status = '{'Pending'}' MATCH (c.User) WHERE b.user = c.username SET c.balance = c.balance + 2 * b.amountBetted SET b.Status = '{'Paid'}'") #reward winners
    graph.run(f"MATCH (b:MoneyLineBet) WHERE b.gameID = {gameId} ") #delete old moneyline bets (including both winning and losing ones)

def Payout_OverUnder_Bet(currentDate, username, isOver):
    graph.run(f"MATCH 

#Rewarding over\under bets will be difficult until I fully understand RavenDB -Josh Mestemacher

def Add_Friend(userUsername, userFriendUsername): #note that I assume both usernames are 
    #actual usernames in the system here, I may go back and change this later.
    graph.run(f"MATCH (u1:User), (u2:User) WHERE u1.username = '{userUsername}' AND u2.username = '{userFriendUsername}' CREATE (u1)-[r:friend_of]->(u2)")

def Remove_Friend(userUsername, userFriendUsername):
    #note that I assume both usernames are 
    #actual usernames in the system here and that the inputted friend 
    #actually is a friend of the user for simplicity's sake for the demo, I may go
    #back and change this later
    graph.run(f"MATCH (u.User) WHERE u.username = {userUsername} AND EXISTS(u.friends) SET n.friends = [x IN n.friends WHERE x <> '{userFriendUsername}']")


def getUsers():
    cursor = graph.run(f"MATCH (u.User) RETURN u.username, u.fullName, [(u)-[r:friend_of]-(C:User)|C.username] AS Friends")
    return cursor.data()

def checkIfBetPlaced_MoneyLineBet(username, gameId):
    cursor = graph.run(f"MATCH (n:MoneyLineBet) WHERE n.gameID = '{gameId}' AND n.user = '{username}'  RETURN COUNT(n)")
    if(cursor.evaluate() > 0):
        return True
    else:
        return False

def checkIfBetPlaced_OrderUnder(username, gameId):
    cursor = graph.run(f"MATCH (n:OverUnderBetPlayer) WHERE n.gameID = '{gameId}' AND n.user = '{username}'  RETURN COUNT(n)")
    if(cursor.evaluate() > 0):
        return True
    else:
        return cursora s

def DeleteOverUnderBet(gameID, username):
    graph.run(f"MATCH (n:OverUnderBet) WHERE n.gameID = '{gameID} AND  n.user = '{username}' DETACH DELETE A)
    
    trnfs mMATCH (u:User) WHERE u.username = n.user SET u.balance = u.balance + n.AmountBetted DETACH DELETE n")

def DeleteMoneyLineBet(BetID):
    graph.run(f"MATCH (n:MoneyLineBet) WHERE n.betId = '{BetID}' MATCH (u:User) WHERE u.username = n.user SET u.balance = u.balance + n.AmountBetted DETACH DELETE n")








