from rhino_v2_utilis.handler.redis_handler import CRedisHandler
import config
import json
from setting import redis_client




redis_client.hset("test:redis","123","443344")

