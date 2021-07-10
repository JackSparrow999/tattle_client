from poc.redis_client import redis_obj

def publish():
    redis_obj.publish('hello_world', 'hello_redis')