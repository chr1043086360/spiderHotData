import redis
from core.settings import HOST_IP, REDIS_PASSWORD

r = redis.StrictRedis(host=f'{HOST_IP}', port=6379, password=f'{REDIS_PASSWORD}')

r.set("foo", "bar")

print(r.get('foo'))