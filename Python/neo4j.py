from matplotlib.backend_bases import GraphicsContextBase
from py2neo import Graph



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







