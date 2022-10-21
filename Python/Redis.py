import bcrypt
import redis
import datetime
def ConnectRedis():
        global r
        r = redis.Redis(
            host='433-17.csse.rose-hulman.edu',
            port=6379,
            decode_responses=True)
def CreateUser(name, username, password, birthday):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()

    hashPassword = bcrypt.hashpw(password.encode("utf-8"), passwordSalt)
    #r.sadd(f'UsernameSalt:{username}', passwordSalt) #this and below line may not need anymore, didn't remove bc didn't know what they are for -Josh
    #r.sadd(f'UsernamePassword:{username}', hashPassword)

    if r.sismember(f'users', username):
        raise ValueError('Username not unique')
    r.sadd(f'users', username)
    r.hset(username, 'passwordHash', hashPassword)
    r.hset(username, 'birthday', birthday.strftime("%d-%m-%Y"))
    r.hset(username, 'name', name)
    #r.hset(username, 'balance', 1000, 'Bets', 0) #don't know if need this as we didn't agree for bets and balances to be put in Redis
def ChangeUserInformation(field, value):
    print('x')

if __name__ == '__main__':
    ConnectRedis()
    #r.hset(f'book:1', 'ISBN', 1)
    print(r.keys("*"))

def loginCheck(username, password):
    if(r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if(bcrypt.checkpw(password.encode("utf-8"), correctPasswordHash.encode("utf-8"))):
            return True
    return False