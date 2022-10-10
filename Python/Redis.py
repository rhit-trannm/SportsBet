import bcrypt
import redis
def ConnectRedis():
        global r
        r = redis.Redis(
            host='433-17.csse.rose-hulman.edu',
            port=6379,
            decode_responses=True)
def CreateUser(username, password):
    #User key format: User_{Username}
    passwordSalt = bcrypt.gensalt()

    hashPassword = bcrypt.hashpw(password, passwordSalt)
    r.sadd(f'UsernameSalt:{username}', passwordSalt)
    r.sadd(f'UsernamePassword:{username}', hashPassword)
    r.hset(f'User:{username}', 'balance', 'nil', 'Bets', 'nil')
def ChangeUserInformation(field, value):
    print('x')

if __name__ == '__main__':
    ConnectRedis()
    #r.hset(f'book:1', 'ISBN', 1)
    print(r.keys("*"))

def loginCheck(username, password, r):
    username = input('enter username')
    password = input('enter password')
    if(r.sismember('users', username)):
        correctPasswordHash = r.hget(username, 'passwordHash')
        if(bcrypt.checkpw(password, correctPasswordHash)):
            loggedIn = True