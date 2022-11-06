import bcrypt
import redis
import datetime


class User(object):
    def __init__(self, username, hashPassword, balance=0, betID=[]):
        self.username = username
        self.hashPassword = hashPassword
        self.balance = balance
        self.betID = betID


def ConnectRedis():
        global r
        r = redis.Redis(
            host='433-17.csse.rose-hulman.edu',
            port=6378)

def Ping():
    r.ping()

def CheckUser(username):
    return r.sismember('users', username)
    
def CreateUser(name, username, password, birthday):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()

def GetUser(username):
    if (r.sismember('users', username)):
        print(r.hgetall(username))
        result = r.hgetall(username)
        return User(username = username, hashPassword=result['passwordHash'])


def CreateUser(name, username, password, birthday):
    # User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    #r.sadd(f'UsernameSalt:{username}', passwordSalt) #this and below line may not need anymore, didn't remove bc didn't know what they are for -Josh
    #r.sadd(f'UsernamePassword:{username}', hashPassword)

    if r.sismember(f'users', username):
        raise ValueError('Username not unique')
    r.sadd(f'users', username)
    r.hset(username, 'passwordHash', hashPassword)
    r.hset(username, 'birthday', birthday)
    r.hset(username, 'name', name)
    #r.hset(username, 'balance', 1000, 'Bets', 0) #don't know if need this as we didn't agree for bets and balances to be put in Redis

def UpdateUser(name, username, password, birthday):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    r.hset(username, 'passwordHash', hashPassword)
    r.hset(username, 'birthday', birthday)
    r.hset(username, 'name', name)


def DeleteUser(username):
    r.srem('users', username)
    r.delete(username)

    # r.sadd(f'UsernameSalt:{username}', passwordSalt) #this and below line may not need anymore, didn't remove bc didn't know what they are for -Josh
    # r.sadd(f'UsernamePassword:{username}', hashPassword)
    if CheckConnection() == 1:
        if r.sismember(f'users', username):
            raise ValueError('Username not unique')
        r.sadd(f'users', username)
        r.hset(username, 'passwordHash', hashPassword)
        r.hset(username, 'birthday', birthday.strftime("%d-%m-%Y"))
        r.hset(username, 'name', name)
        return 1
    else:
        return 0
    # r.hset(username, 'balance', 1000, 'Bets', 0) #don't know if need this as we didn't agree for bets and balances to be put in Redis


def ChangeUserInformation(field, value):
    print('x')


if __name__ == '__main__':
    ConnectRedis()
    #CreateUser("Billy", "billyn", "passowrd123", "11-21-2002")
    # r.hset(f'book:1', 'ISBN', 1)
    # print(GetUser("billyn"))
    # print(r.keys("*"))


def loginCheck(username, password):
    if(r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if(bcrypt.checkpw(password.encode("utf-8"), correctPasswordHash)):
            return True
    return False
