from matplotlib.backend_bases import GraphicsContextBase
from py2neo import Graph
import bcrypt
from regex import F



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

def login_Check(username, password):
   userExists = graph.run(f"MATCH (u:User) WHERE User.username = {username} WITH COUNT(u) > {0} as node_exists RETURN node_exists")
   if(userExists):
    correctPassword = graph.run(f"MATCH(User) WHERE User.username = {username} RETURN User.passwordHash")
    if(password == correctPassword):
        return True


   # if(r.sismember('users', username)):
    #    correctPassword = r.hget(username, 'password')
     #   if(password == correctPassword):
      #      return True




