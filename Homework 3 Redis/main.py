# This is a sample Python script.
import redis
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def connectRedis():
    global r
    r = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True)
    values = r.get('foo')
    value = r.smembers('myClass')
    print(f'{value} {values}')
def getallKeys():
    keys = r.keys('*book*')
    for key in keys:
        print(key);
def addBook(title, ISBN, pages, authors):
    #sets so it sortable
    # r.sadd('book', ISBN)
    # r.sadd(f'book:{ISBN}:title', title)
    #
    # r.sadd(f'book:{ISBN}:author', author)
    # r.sadd(f'book:{ISBN}:pages', pages)

    #https://stackoverflow.com/questions/31266743/how-to-sort-a-redis-hash-by-values-in-keys
    r.hset(f'book:{ISBN}','ISBN', ISBN)
    r.hset(f'book:{ISBN}','title', title)
    r.hset(f'book:{ISBN}','pages', pages)
    i = 0
    for author in authors:
        #r.hset(f'book:{ISBN}', f'author{i}', author)
        #index for author
        r.sadd(f'author:{ISBN}', author)
        r.sadd(f'book:{author}', ISBN)
    #Search by title, author, or isbn.
    #Maintain index for those.
    r.sadd(f'book:{title}', ISBN)

def editBook(ISBN, field, value):
    if field == 'author':
        r
    else:
        r.hset(f'book:{ISBN}', field, value)
def deleteBook(ISBN):
    #delete title index
    r.delete(f'book:{r.hget(f"book:{ISBN}", "title")}')
    #delete author-ISBN index
    for author in r.get(f'author:{ISBN}'):
        r.delete(f'book:{author}')
    #delete ISBN-author index
    r.delete(f'author:{ISBN}')
    #delete ISBN from library
    r.delete(f"book:{ISBN}")

def searchBook():


def returnSorted():
def addBorrower():
def deleteBorrower():
def editBorrower():
def searchBorrower():
def checkoutBook():


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    connectRedis()
    # addBook("Queens Gambit", "223", "100", ['Gamb', 'Gamb1'])
    # addBook('Bob"s playplace', '224', '101',['Bob', 'Builder'])
    # addBook('Zob"s playplace', '225', '103', ['Zob', 'Builder'])
    getallKeys()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
