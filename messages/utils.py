# We’ll store online users temporarily in Redis

import redis

# Connect to Redis database
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)

# Mark a user as online
def set_user_online(user_id):
    redis_client.sadd('online_users', user_id)

# Mark a user as offline
def set_user_offline(user_id):
    redis_client.srem('online_users', user_id)

# Check if a user is online
def is_user_online(user_id):
    return redis_client.sismember('online_users', user_id)


# We use Redis “sets” to store online user IDs.
# sadd → add to set (user is online)
# srem → remove from set (user is offline)
# sismember → check if user is online