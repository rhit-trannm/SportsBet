import bcrypt
import redis
def ConnectRedis():
        global r
        r = redis.Redis(
            host='433-17.csse.rose-hulman.edu',
            port=6379,
            decode_responses=True)
def CreateUser(username, password, birthday):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()

    hashPassword = bcrypt.hashpw(password, passwordSalt)
    r.sadd(f'UsernameSalt:{username}', passwordSalt) #this and below line may not need anymore, didn't remove bc didn't know what they are for -Josh
    r.sadd(f'UsernamePassword:{username}', hashPassword)

    if r.sismember(f'users', username):
        raise Exception('Username not unique')
    r.sadd(f'users', username)
    r.hset(username, 'passwordHash', hashPassword)
    r.hset(username, 'birthday', birthday)
    r.hset(f'User:{username}', 'balance', 'nil', 'Bets', 'nil') #don't know if need this as we didn't agree for bets and balances to be put in Redis
def ChangeUserInformation(field, value):
    print('x')

if __name__ == '__main__':
    ConnectRedis()
    #r.hset(f'book:1', 'ISBN', 1)
    print(r.keys("*"))

def loginCheck(username, password, r=r):
    username = input('enter username')
    password = input('enter password')
    if(r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if(bcrypt.checkpw(password, correctPasswordHash)):
            return True
    return False