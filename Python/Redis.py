import bcrypt
import redis
import datetime
import RavenDB
def ConnectRedis():
        global r
        r = redis.Redis(
            host='433-17.csse.rose-hulman.edu',
            port=6378)

def Ping():
    r.ping()

def CheckUser(username):
    return r.sismember('users', username)

def GetUser(username):
    if (r.sismember('users', username)):
        print(r.hgetall(username))
        result = r.hgetall(username)
        return RavenDB.User(username = username, hashPassword=result['passwordHash'])


def CreateUser(name, username, password, birthday):
    # User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()
    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)

    if r.sismember(f'users', username):
        raise ValueError('Username not unique')
    r.sadd(f'users', username)
    r.hset(username, 'passwordHash', hashPassword)
    r.hset(username, 'birthday', birthday)
    r.hset(username, 'name', name)

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

def ChangeUserInformation(field, value):
    print('x')


if __name__ == '__main__':
    ConnectRedis()


def loginCheck(username, password):
    if(r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if(bcrypt.checkpw(password.encode("utf-8"), correctPasswordHash)):
            return True
    return False
