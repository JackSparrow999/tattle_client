from poc.redis_client import redis_util


if __name__ == "__main__":
    print("Starting poc /-")
    redis_util.set('ronaq', 'raja')
    print(redis_util.get('ronaq'))