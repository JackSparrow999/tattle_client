import redis

redis_util = redis.Redis(host='127.0.0.1', port=6379, db=0, decode_responses=True)

