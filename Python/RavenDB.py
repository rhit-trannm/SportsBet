from pyravendb.store import document_store
from Python import main as API

def StoreObject(object):
    with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
        store.initialize()
        with store.open_session() as session:
            session.store(object)
            session.save_changes()
if __name__ == '__main__':
    player = API.GetPlayerStats(203076)
    print(player.PLAYER_ID)
    StoreObject(player)
    # with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
    #     store.initialize()
    #     print("hello 2")
    #     with store.open_session() as session:
    #         print("hello world")
    #         foo = Foo("PyRavenDB")
    #         session.store(foo)
    #         session.save_changes()
