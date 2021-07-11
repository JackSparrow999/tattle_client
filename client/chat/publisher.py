from client.chat.redis_client import redis_obj

def publish_chat(chat):
    if chat == None:
        return
    redis_obj.publish('chat_channel', chat)