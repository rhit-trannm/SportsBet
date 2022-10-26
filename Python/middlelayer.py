from Python import neo4j
from Python import RavenDB
from py2neo import Graph
from pyravendb.store import document_store
#Principles When coding middle layer:
#Read does not need to get written to file
#Write needs to get written to file

#routing logic: Ping each database before performing action. Check if they are up.
#Check if up to date,
#If it is not -> reroute and update it while rerouting.
#If it is -> Use database.

#User -> Duplicated on all 3 database. Should follow this roadmap... Redis -> Neo4j -> RavendB
#Bets -> Duplicated on Neo4J and RavenDB. Neo4J -> RavenDB.
#NBA Teams/Player info -> On RavenDB. Should never go down.

#In general, RavenDB should never go down. If it does go down, the entire system should go down.


if __name__ == '__main__':
    print('x')