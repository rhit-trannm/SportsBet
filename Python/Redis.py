import bcrypt
import redis
def ConnectRedis():
    def ConnectRedis():
        global r
        r = redis.Redis(
            host='localhost',
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
    print('x')