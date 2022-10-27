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
