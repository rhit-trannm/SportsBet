import json

from py2neo import Graph
import bcrypt

class User(object):
    def __init__(self, username, hashPassword, balance=0, betID=[]):
        self.username = username
        self.hashPassword = hashPassword
        self.balance = balance
        self.betID = betID

def ConnectNeo4J():
    global graph
    graph = Graph("bolt://433-14.csse.rose-hulman.edu:7687", auth=("neo4j", "433-15")) #EDIT THIS TO BE ACCURATE -Josh Mestemacher

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

def Get_Friend_List(username):
    cursor  = graph.run(f"MATCH (User1)-[r:friend_of]-(u:User2)\nWHERE User1.username = '{username}' \nRETURN u")
    numberOfFriends = Get_Number_Of_Friends(username)
    if(numberOfFriends == 0):
        return None; #change this if need be to work with front end
    data = [record for record in cursor.data()]
    friendList = [None] * numberOfFriends
    for i in range(0, numberOfFriends):
        friendList[i] = data[i]['u'].get('username') #returned friend list will be list of usernames, change if necessary
    return friendList

def GetUser(username):
    dataset = graph.run(f"MATCH (n:Person {{username : '{username}'}}) RETURN n").data()
    if dataset != []:
        #print(json.loads(json.dumps(dataset.pop()['n'])))
        return json.loads(json.dumps(dataset.pop()['n']))
        #return dataset.pop()['n']

def Create_User(name, username, password, birthday):
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    graph.run(f"CREATE (n:Person {{username: '{username}', passwordHash: '{hashPassword.decode()}', balance: {0}, fullName: '{name}', birthday: '{birthday}'}})")

def Login_Check(username, password):
   userExists = graph.run(f"MATCH (u:User) WHERE u.username = '{username}' WITH COUNT(u) > {0} as node_exists RETURN node_exists")
   if(userExists):
    cursor = graph.run(f"MATCH(User) WHERE User.username = '{username}' RETURN User.passwordHash")
    passwordHash = cursor.evaluate()
    if bcrypt.checkpw(password.encode("utf-8"), passwordHash.encode("utf-8")):
        return True
    else:
        return False
if __name__ == '__main__':
    ConnectNeo4J()
    #Create_User("billy", "billy2", "billa", "10-2-22")
    GetUser("billy2")

def Create_MoneyLine_Bet(game_date, winner_team_abbrev, amount_betted, username, matchId, betId): #I assume team abbrev is a drop down for this,  and so is matchId and game_date you can pass in user generated name for betId
    ConnectNeo4J
    userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:MoneyLineBet {{user: '{username}', amountBetted: '{amount_betted}', winnerAbbrev: '{winner_team_abbrev}', game_date: '{game_date}', gameID: '{matchId}', betID: '{betId}'}})")
            graph.run(f"MATCH (u:User) WHERE u.username = {username} SET u.balance = u.balance - {amount_betted}") #adjust user balance,

def Create_OverUnder_Bet_Team(game_date, amount_betted, username, isUnder, points_bet, matchId, teamId, betId): #isUnder is 1 or 0 (meaning its an over bet), I assume isUnder will be a drop down
    #box, I assume amount_betted will be an integer. points_bet is amount you are betting point count for a team will be under or over, technically in real betting not controlled by you
    #I assume gameId and game_date and teamId is point and click or drop done or automatically determined by ravenDb and sent here as inputs. you can pass in user generated name for betId
    userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
    if(userExists):
        if(amount_betted > 0):
            #actually create bet, will implement balance checking here sometime soon,
            graph.run(f"CREATE (n:OverUnderBet {{user: '{username}', amountBetted: '{amount_betted}', teamId: '{teamId}', isUnder: '{isUnder}', game_date: '{game_date}', points_bet: '{points_bet}', matchId: '{matchId}', betID:'{betId}'}})")
            graph.run(f"MATCH (u:User) WHERE u.username = {username} SET u.balance = u.balance - {amount_betted}") #adjust user balance,

def DeleteOverUnderBet(BetId):
    graph.run(f"MATCH (n:OverUnderBet) WHERE n.betId = '{BetId}' MATCH (u:User) WHERE u.username = n.user SET u.balance = u.balance + n.AmountBetted DETACH DELETE n")

def DeleteMoneyLineBet(BetID):
    graph.run(f"MATCH (n:MoneyLineBet) WHERE n.betId = '{BetID}' MATCH (u:User) WHERE u.username = n.user SET u.balance = u.balance + n.AmountBetted DETACH DELETE n")

def Payout_MoneyLine_Bets(currentDate, winningTeamAbbrev): #we assume a team can't play 2 games in one day for this method, going with double payout for now for simplicity's sake - Josh Mestemacher
    graph.run(f"MATCH (b.MoneyLineBet) WHERE b.data < {currentDate} AND b.winnerAbbrev = {winningTeamAbbrev} WITH C MATCH (u.User) WHERE C.user = u.username SET u.balance = u.balance + 2 * b.amountBetted") #reward winners
    graph.run(f"MATCH (b.MoneyLineBet) WHERE b.data < {currentDate} DETACH DELETE b") #delete old moneyline bets (including both winning and losing ones)

#Rewarding over\under bets will be difficult until I fully understand RavenDB -Josh Mestemacher

def Add_Friend(userUsername, userFriendUsername): #note that I assume both usernames are 
    #actual usernames in the system here, I may go back and change this later.
    graph.run(f"MATCH (u1:Person), (u2:Person) WHERE u1.username = '{userUsername}' AND u2.username = '{userFriendUsername}' CREATE (u1)-[r:friend_of]->(u2)")

def Remove_Friend(userUsername, userFriendUsername):
    #note that I assume both usernames are 
    #actual usernames in the system here and that the inputted friend 
    #actually is a friend of the user for simplicity's sake for the demo, I may go
    #back and change this later
    graph.run(f"MATCH (u.User) WHERE u.username = {userUsername} AND EXISTS(u.friends) SET n.friends = [x IN n.friends WHERE x <> '{userFriendUsername}']")



