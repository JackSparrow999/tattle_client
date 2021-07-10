from poc.redis_client import redis_obj
import poc.publisher as pub
import poc.subscriber as sub
import time

if __name__ == "__main__":
    print("Starting poc /-")

    while True:
        pub.publish()
        time.sleep(1)