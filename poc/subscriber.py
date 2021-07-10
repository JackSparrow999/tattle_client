from poc.redis_client import redis_obj

def message_handler(message):
    if message == None:
        return None

    print(message["data"])

pub = redis_obj.pubsub()
pub.subscribe(**{'hello_world': message_handler})

thread = pub.run_in_thread(sleep_time=1)