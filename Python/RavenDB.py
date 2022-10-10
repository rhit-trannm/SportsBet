from pyravendb.store import document_store
class Foo(object):
   def __init__(self, name, key = None):
       self.name = name
       self.key = key

class FooBar(object):
    def __init__(self, name, foo):
        self.name = name
        self.foo = foo

if __name__ == '__main__':
    with document_store.DocumentStore(urls=["http://137.112.104.162:8080"], database="temp") as store:
        store.initialize()
        print("hello 2")
        with store.open_session() as session:
            print("hello world")
            foo = Foo("PyRavenDB")
            session.store(foo)
            session.save_changes()
