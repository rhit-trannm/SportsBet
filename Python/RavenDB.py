from pyravendb.store import document_store
from Python import main as API
import bcrypt
from nba_api.stats.endpoints import commonplayerinfo, leaguegamefinder, scoreboardv2, playercareerstats, commonteamroster
from nba_api.stats.static import teams, players
class User(object):
    def __init__(self, username, hashPassword, balance = 0, betID = []):
        self.username = username
        self.hashPassword = hashPassword
        self.balance = balance
        self.betID = betID

def CreateUser(username, password):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password, passwordSalt)
    temp = User(username, password)
    with document_store.DocumentStore(urls=["http://127.0.0.1:8080"], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(temp)
            session.save_changes()
def StoreObject(object):
    with document_store.DocumentStore(urls=["http://127.0.0.1:8080"], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(object)
            session.save_changes()
if __name__ == '__main__':
    #player = API.GetPlayerStats(203076)
    #print(player.PLAYER_ID)
    nba_players = players.get_active_players()
    for player in nba_players:
        if player['id'] is not None:
            temp = API.GetPlayerStats(player['id'])
            if temp is not None:
                StoreObject(temp)

    # with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
    #     store.initialize()
    #     print("hello 2")
    #     with store.open_session() as session:
    #         print("hello world")
    #         foo = Foo("PyRavenDB")
    #         session.store(foo)
    #         session.save_changes()
