import redis
import random
import time

redis_obj = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

def publish():
    s = 'hello_redis' + str(random.randint(1, 10))
    print("Publishing: " + s)
    redis_obj.publish('hello_world', s)

if __name__ == '__main__':

    while True:
        publish()
        time.sleep(2)