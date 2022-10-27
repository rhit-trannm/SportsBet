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
    global r, serverList
    serverList = ['localhost', '433-14.csse.rose-hulman.edu', '433-15.csse.rose-hulman.edu',
                  '433-16.csse.rose-hulman.edu', '433-17.csse.rose-hulman.edu']
    # while True:
    index = 1
    r = redis.Redis(
        host=serverList[index],
        port=6379,
        decode_responses=True)


def CheckConnection():
    try:
        ConnectRedis()
        r.ping()
        return 1
    except:
        return 0


def GetUser(username):
    if (r.sismember('users', username)):
        print(r.hgetall(username))
        result = r.hgetall(username)
        return User(username = username, hashPassword=result['passwordHash'])


def CreateUser(name, username, password, birthday):
    # User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
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


def LoginCheck(username, password):
    if (r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if (bcrypt.checkpw(password.encode("utf-8"), correctPasswordHash.encode("utf-8"))):
            return True
    return False
