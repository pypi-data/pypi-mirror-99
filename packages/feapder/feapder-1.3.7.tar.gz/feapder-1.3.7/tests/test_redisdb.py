from feapder.db.redisdb import RedisDB

db = RedisDB.from_url("redis://localhost:6379")

# db = RedisDB(ip_ports="172.25.21.4:26379,172.25.21.5:26379,172.25.21.6:26379", db=0, user_pass=None)

db.zadd("test", list(range(10)), list(range(10)))

# db.zremrangebyscore("test", 1, 3)

db.zrem("test", [4, 0])

print(db.zget("test", 10))

